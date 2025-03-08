from config import *

###########################################################
## Simple function to call the DevOps API and get the latest 
## manual intervention for the release
###########################################################
def getInterventionId(build_id, stage_id):
    req = requests.post(
        url     = VALIDATION_URL.format(ORGANIZATION, PROJECT),
        headers = AZDO_HEADER,
        data    = json.dumps(dict(
            contributionIds = ["ms.vss-build-web.checks-panel-data-provider"],
            dataProviderContext = dict(
                properties = dict(
                    buildId = build_id,
                    stageIds = stage_id,
                    checkListItemType = 3,
                    sourcePage = dict(
                        url = "https://dev.azure.com/{}/{}/_build/results?buildId={}&view=logs".format(ORGANIZATION, PROJECT, build_id),
                        routeId = "ms.vss-build-web.ci-results-hub-route",
                        routeValues = dict(
                            project = PROJECT,
                            viewname = "build-results",
                            controller = "ContributedPage",
                            action = "Execute",
                            serviceHost = ORGANIZATION_ID
                        ),
                    ),
                ),
            ),
        )),
    )
    return(json.loads(req.content)["dataProviders"]["ms.vss-build-web.checks-panel-data-provider"][0]["manualValidations"][0]["id"])
