from datetime import datetime


def checksWithRules( contest, rule, data, submitter):
    result = dict()
    if rule["namespaceMain"]:
        result["namespaceMain"] = {
            "expected": True,
            "actual": data["page_ns"] == 0,
            "check": data["page_ns"] == 0
        }

    if rule["pageSize"]["status"]:
        mode = rule["pageSize"]["mode"]

        expectedSize = None
        actualSize = None
        if mode == "bytes":
            expectedSize = rule["pageSize"]["bytes"]
            actualSize = data["page_size"]
        elif mode == "words":
            actualSize = data["page_words"]
            expectedSize = rule["pageSize"]["words"]

        result["pageSize"] = {
            "mode": mode,
            "expected": expectedSize,
            "actual": actualSize,
            "check": expectedSize <= actualSize
        }

    if rule["creationInRange"]:
        startDate = contest.start_date
        endDate = contest.end_date
        createDate = datetime.strptime(data["pageCreatedAt"], "%Y-%m-%dT%H:%M:%SZ")
        isWithIn = startDate <= createDate <= endDate

        result["creationInRange"] = {
            "expected": True,
            "actual": isWithIn,
            "check": isWithIn
        }

    if rule["submitterRegDate"]["status"]:
        exptDate = datetime.strptime( rule["submitterRegDate"]["value"], "%Y-%m" )
        actDate = datetime.strptime( data["userRegdata"], "%Y-%m-%dT%H:%M:%SZ" )
        result["submitterRegDate"] = {
            "expected":  exptDate.isoformat(),
            "actual": actDate.isoformat(),
            "check": actDate <= exptDate
        }

    if rule["authorOnly"]:
        result["authorOnly"] = {
            "expected": submitter,
            "actual": data["pageCreatedBy"],
            "check": submitter == data["pageCreatedBy"]
        }

    if rule["pageSizeBySubmitter"]["status"]:
        exptSize = rule["pageSizeBySubmitter"]["bytes"]

        # Summing the revision's size
        actualSize = 0
        try:
            for i in data["contributions"][submitter]:
                actualSize += i["sizediff"]
        except:
            pass

        result["pageSizeBySubmitter"] = {
            "mode": "bytes",
            "expected": exptSize,
            "actual": actualSize,
            "check": exptSize <= actualSize
        }

    if rule["minImages"]["status"]:
        exptImages = int( rule["minImages"]["value"] )
        actImages = data["pageImages"]
        result["minImages"] = {
            "expected": exptImages,
            "actual": actImages,
            "check": exptImages <= actImages
        }

    if rule["minTemplates"]["status"]:
        exptTemps = int( rule["minTemplates"]["value"] )
        actTemps = data["pageTemplate"]
        result["minTemplates"] = {
            "expected": exptTemps,
            "actual": actTemps,
            "check": exptTemps <= actTemps
        }

    if rule["minCategories"]["status"]:
        exptCats = int( rule["minCategories"]["value"] )
        actCats = data["pageTemplate"]
        result["minCategories"] = {
            "expected": exptCats,
            "actual": actCats,
            "check": exptCats <= actCats
        }

    if rule["minLangLinks"]["status"]:
        exptLinks = int( rule["minLangLinks"]["value"] )
        actLinks = data["pageTemplate"]
        result["minLangLinks"] = {
            "expected": exptLinks,
            "actual": actLinks,
            "check": exptLinks <= actLinks
        }

    return result