# Deploy to Azure App Service

This file is the setup for when the Azure account exists. The workflow in `.github/workflows/deploy.yml` is already on `main`. Until you set the GitHub variable `AZURE_DEPLOY_ENABLED` to `true`, a push runs the build and skips both deploy jobs. Nothing here is tied to one site's name. Copy these files to Plato2–Plato10 and repeat the steps that contain `<REPO>`.

`<REPO>` is the repository name only, such as `Plato9`. The owner is `Gooberin95`.

## What the pipeline does

The `build` job runs on every push to `main` and on **Run workflow**. It installs Python from `.python-version`, plus Node.js and Bun, because Reflex compiles the pages in Python and then bundles them with that JavaScript toolchain. The command is:

```bash
reflex export --env prod --frontend-only --no-zip
```

That writes the static site to `.web/build/client`. The job packs the Python app, `requirements.txt`, `startup.sh`, `serve_prod.py`, `assets/`, and that static build. It does not pack `node_modules`, `package.json`, or a virtualenv. The result is the `app` artifact.

`deploy-staging` needs `build`, uses the GitHub environment `staging`, and deploys that artifact. `deploy-production` needs `deploy-staging`, uses the environment `production`, and deploys the same artifact. Both jobs log in with OpenID Connect (no stored Azure password) and deploy with `azure/webapps-deploy`. Both are skipped unless `AZURE_DEPLOY_ENABLED` is exactly `true`.

Add yourself as a required reviewer on the `production` environment. After staging is updated, GitHub waits for your approval before production starts.

## Python on App Service, without Docker

Yes. Azure App Service on Linux has a built-in Python 3.14 runtime. Create the app with `PYTHON|3.14`. You do not need a container image.

Microsoft documents the stack here: [Configure Linux Python apps](https://learn.microsoft.com/en-us/azure/app-service/configure-language-python). The announcement that 3.14 is a first-class runtime is [Python 3.14 is now available on Azure App Service for Linux](https://azure.github.io/AppService/2025/10/28/python314-available.html) (28 October 2025).

App Service does not pin the patch. `PYTHON|3.14` tracks the latest 3.14 patch on the platform image. On 22 October 2026 the built-in image was updated to **Python 3.14.9** ([emergency runtime update](https://azure.github.io/AppService/2026/10/22/node-python-emergency-release-app-service-linux.html)). This project was developed on 3.14.4. Reflex 0.10.0 accepts Python `>=3.11, <4`, so 3.14.9 runs it. A custom Docker image would be how you pin 3.14.4 exactly. This pipeline does not do that.

Check the token on your subscription before you create the apps:

```bash
az webapp list-runtimes --os linux | grep PYTHON
```

Use the `PYTHON|3.14` line that command prints.

## One port, and why startup is not `reflex run`

`reflex run --help` includes `--env [dev|preview|prod]` and `--single-port`. `--single-port` is only valid with `--env prod`. In that mode Reflex does serve the site and the backend on one port. It also **rebuilds** the frontend on every start (`reflex export` is the same JavaScript build). The App Service Python image does not include Node or Bun, so that command cannot be the startup command.

CI runs the build once. `startup.sh` then runs `python serve_prod.py`, which:

- sets production mode
- skips the frontend compile (`REFLEX_SKIP_COMPILE`)
- mounts `.web/build/client` on the ASGI app (`REFLEX_MOUNT_FRONTEND_COMPILED_APP`)
- listens on `0.0.0.0` and `${PORT:-${WEBSITES_PORT:-8000}}` with Granian, one worker

The exported client calls `http://localhost:8000`. Reflex rewrites `localhost` to the hostname in the browser. On Azure's HTTPS address the socket is `wss` on port 443, so the same artifact works for staging and production. Leave the API URL at that default. Do not bake an Azure hostname into the build.

Set `WEBSITES_PORT` to `8000` so the App Service front end forwards to the port the process opens.

## Dependencies: Oryx installs them

Ship source and a prebuilt frontend. Let Oryx install Python packages during deployment.

A virtualenv built on a GitHub runner is not portable. Its `python` path and shebangs point at the runner, and App Service looks for an environment named `antenv` built for its own interpreter. Microsoft's guidance is to keep the virtualenv out of the zip and set `SCM_DO_BUILD_DURING_DEPLOYMENT` so Oryx runs `pip install -r requirements.txt` on the Python 3.14 image: [Configure Linux Python apps](https://learn.microsoft.com/en-us/azure/app-service/configure-language-python) (see the build-automation steps and the `ModuleNotFoundError` note about deploying your own virtualenv).

`requirements.txt` contains `reflex==0.10.0`. Reflex's Linux wheels cover Python 3.14, and Oryx installs them when you deploy, not on every start. The artifact has no root `package.json`, so Oryx does not try to run a Node build. The JavaScript is already in `.web/build/client`.

The startup command is the file name:

```text
startup.sh
```

App Service runs that after Oryx has activated the virtualenv.

## 1. Install the Azure CLI and log in

On Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl apt-transport-https lsb-release gnupg
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az version
az login
```

`az login` opens a browser. When it finishes:

```bash
az account show --output table
```

If you have more than one subscription, select the new one. Copy the subscription id from the first command, or use the name:

```bash
az account set --subscription "<subscription name or id>"
az account show --query "{name:name, id:id, tenant:tenantId}" --output json
```

Leave this terminal open. Later steps use `id` as the subscription id and `tenant` as the tenant id.

If the first `az webapp create` says the namespace is not registered:

```bash
az provider register --namespace Microsoft.Web --wait
```

## 2. One resource group and one Linux plan

Basic B1 has no deployment slots. Staging and production are two web apps on the same plan. The other Plato sites can use this same plan: two apps per repository, twenty apps if you deploy all ten. B1 is a small machine. If a site is slow, scale the plan up; you do not need a second plan to get a second app.

Names below are suggestions for the shared resources. Web app names are global across Azure, so they have to be unique. Use lowercase.

```bash
LOCATION="westeurope"
RG="plato-sites"
PLAN="plato-linux"

az group create --name "$RG" --location "$LOCATION"

az appservice plan create \
  --name "$PLAN" \
  --resource-group "$RG" \
  --sku B1 \
  --is-linux
```

Change `LOCATION` if you want a different region. The plan and every app in it share that region.

## 3. Create the two web apps

Replace `<REPO>` with the lowercase repository name (`plato9` for this repo). Azure web app names allow letters, numbers, and hyphens.

```bash
REPO_SLUG="plato9"    # lowercase. Plato2 becomes plato2, and so on.
WEBAPP_STAGING="${REPO_SLUG}-staging"
WEBAPP_PRODUCTION="${REPO_SLUG}-prod"

az webapp create \
  --resource-group "$RG" \
  --plan "$PLAN" \
  --name "$WEBAPP_STAGING" \
  --runtime "PYTHON|3.14"

az webapp create \
  --resource-group "$RG" \
  --plan "$PLAN" \
  --name "$WEBAPP_PRODUCTION" \
  --runtime "PYTHON|3.14"
```

If `--runtime` rejects that token, run `az webapp list-runtimes --os linux` and pass the Python 3.14 value it prints.

Configure each app. This sets the Python stack again, the startup file, websockets, and the Oryx flags. Websockets are required: Reflex state uses a Socket.IO connection, and App Service drops that traffic when websockets are off.

```bash
configure_app() {
  local name="$1"
  az webapp config set \
    --resource-group "$RG" \
    --name "$name" \
    --linux-fx-version "PYTHON|3.14" \
    --startup-file "startup.sh" \
    --web-sockets-enabled true

  az webapp config appsettings set \
    --resource-group "$RG" \
    --name "$name" \
    --settings \
      SCM_DO_BUILD_DURING_DEPLOYMENT=true \
      ENABLE_ORYX_BUILD=true \
      WEBSITES_PORT=8000
}

configure_app "$WEBAPP_STAGING"
configure_app "$WEBAPP_PRODUCTION"
```

Confirm one app before you continue:

```bash
az webapp config show \
  --resource-group "$RG" \
  --name "$WEBAPP_STAGING" \
  --query "{stack:linuxFxVersion, startup:appCommandLine, websockets:webSocketsEnabled}" \
  --output json
```

`stack` is `PYTHON|3.14`, `startup` is `startup.sh`, and `websockets` is `true`.

The starred schedule, the pass hold, and the countdown live in Reflex state on that instance. They are not saved to a database, and the hold does not charge a card. Oryx runs the app from a deploy directory that is replaced on the next deploy, so that session state does not survive a new deploy.

## 4. Entra ID app and federated credentials

GitHub Actions will request a token for this app. Azure will only hand one over when the token's subject matches a federated credential. Create one credential for `environment:staging` and one for `environment:production`. The workflow's `environment:` names and these subjects have to match, including the word `environment`.

One app registration can cover every Plato repository. Add two credentials per repository. The client id, tenant id, and subscription id are then the same secrets in each repo. Contributor on the resource group covers every web app in that group.

```bash
AZ_APP_ID="$(az ad app create --display-name "github-plato-deploy" --query appId --output tsv)"
echo "client id: $AZ_APP_ID"
az ad sp create --id "$AZ_APP_ID"

TENANT_ID="$(az account show --query tenantId --output tsv)"
SUB_ID="$(az account show --query id --output tsv)"
```

Write a credential file. The `name` must be unique on the app registration. The `subject` must use the real repository name.

```bash
REPO="Plato9"   # the GitHub repository name, with its real capital letters

cat > /tmp/github-staging.json <<EOF
{
  "name": "${REPO}-staging",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:Gooberin95/${REPO}:environment:staging",
  "description": "GitHub Actions environment staging for ${REPO}",
  "audiences": ["api://AzureADTokenExchange"]
}
EOF

cat > /tmp/github-production.json <<EOF
{
  "name": "${REPO}-production",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:Gooberin95/${REPO}:environment:production",
  "description": "GitHub Actions environment production for ${REPO}",
  "audiences": ["api://AzureADTokenExchange"]
}
EOF

az ad app federated-credential create --id "$AZ_APP_ID" --parameters /tmp/github-staging.json
az ad app federated-credential create --id "$AZ_APP_ID" --parameters /tmp/github-production.json
rm -f /tmp/github-staging.json /tmp/github-production.json
```

For Plato2, run the two `cat` / `federated-credential create` blocks again with `REPO="Plato2"`. Do not create a second app registration unless you want a separate client id.

Assign Contributor, scoped to the resource group only:

```bash
az role assignment create \
  --assignee "$AZ_APP_ID" \
  --role "Contributor" \
  --scope "/subscriptions/${SUB_ID}/resourceGroups/${RG}"
```

Role assignment can take a minute to show up. If the first deploy returns an authorization error, wait and rerun the workflow.

## 5. GitHub secrets, variables, and environments

Install and log in to the GitHub CLI if you have not (`gh auth login`). The repository must exist, and your user must be allowed to change secrets and environments.

These are the secrets. The names are fixed by the workflow:

| Name | Value |
| --- | --- |
| `AZURE_CLIENT_ID` | The app id printed as `client id` above |
| `AZURE_TENANT_ID` | `$TENANT_ID` |
| `AZURE_SUBSCRIPTION_ID` | `$SUB_ID` |

These are the variables:

| Name | Value |
| --- | --- |
| `AZURE_WEBAPP_NAME_STAGING` | `$WEBAPP_STAGING`, the staging web app name |
| `AZURE_WEBAPP_NAME_PRODUCTION` | `$WEBAPP_PRODUCTION`, the production web app name |
| `AZURE_DEPLOY_ENABLED` | `true`, and only after the environments exist |

Set the secrets and the two name variables. Leave `AZURE_DEPLOY_ENABLED` unset until the environments are in place.

```bash
REPO="Plato9"
gh secret set AZURE_CLIENT_ID --repo "Gooberin95/${REPO}" --body "$AZ_APP_ID"
gh secret set AZURE_TENANT_ID --repo "Gooberin95/${REPO}" --body "$TENANT_ID"
gh secret set AZURE_SUBSCRIPTION_ID --repo "Gooberin95/${REPO}" --body "$SUB_ID"
gh variable set AZURE_WEBAPP_NAME_STAGING --repo "Gooberin95/${REPO}" --body "$WEBAPP_STAGING"
gh variable set AZURE_WEBAPP_NAME_PRODUCTION --repo "Gooberin95/${REPO}" --body "$WEBAPP_PRODUCTION"
```

Create the environments in the browser so the production rule is visible:

1. Open `https://github.com/Gooberin95/<REPO>/settings/environments`.
2. Choose **New environment**. Name it `staging`. Create it. Add no protection rule.
3. Choose **New environment** again. Name it `production`.
4. Turn on **Required reviewers**. Add yourself. Save.

The names `staging` and `production` are exact. A different name will not match the workflow or the federated subject.

You can create them from the CLI instead. `prevent_self_review` stays false so the person who pushed can still approve.

```bash
REPO="Plato9"
gh api --method PUT -H "Accept: application/vnd.github+json" \
  "/repos/Gooberin95/${REPO}/environments/staging" \
  --input - <<'EOF'
{"wait_timer": 0}
EOF

USER_ID="$(gh api user --jq .id)"
gh api --method PUT -H "Accept: application/vnd.github+json" \
  "/repos/Gooberin95/${REPO}/environments/production" \
  --input - <<EOF
{
  "reviewers": [{"type": "User", "id": ${USER_ID}}],
  "prevent_self_review": false
}
EOF
```

Then turn deploys on and start a run:

```bash
gh variable set AZURE_DEPLOY_ENABLED --repo "Gooberin95/${REPO}" --body "true"
gh workflow run deploy.yml --repo "Gooberin95/${REPO}" --ref main
gh run watch --repo "Gooberin95/${REPO}"
```

`build` should pass, then `deploy-staging` should deploy. `deploy-production` waits. Open the run in GitHub, review the staging site at `https://<WEBAPP_STAGING>.azurewebsites.net`, and approve the production environment. Production then deploys to `https://<WEBAPP_PRODUCTION>.azurewebsites.net`.

The first request after a deploy can take a little while. Oryx installs Reflex during deployment, and the process still has to import the app. If the site shows the default App Service page, check that `startup.sh` is the startup command and that the deployment log shows pip installing `requirements.txt`.

## Copying this to another Plato repository

Copy `.github/workflows/deploy.yml`, `startup.sh`, `serve_prod.py`, `scripts/package_deploy.sh`, and this file. The workflow reads names only from secrets and variables.

For that repository:

1. Create `<repo-slug>-staging` and `<repo-slug>-prod` on the same plan, and run `configure_app` for each.
2. Add federated credentials for `repo:Gooberin95/<REPO>:environment:staging` and `repo:Gooberin95/<REPO>:environment:production`.
3. Set the three secrets and the two web app name variables on that repo.
4. Create `staging` and `production` environments, with a required reviewer on `production`.
5. Set `AZURE_DEPLOY_ENABLED` to `true` and run the workflow.


