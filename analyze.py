from mwparserfromhell import parse
import requests


class AnalyzePage:
    def __init__(self, contest, page, user):
        self.project = contest.project
        self.lang = contest.language
        self.page = page
        self.user = user

        self.apiEndpoint =  f"https://{self.lang}.{self.project}.org/w/api.php"
        self.header = {
            "User-Agent": "WikiContest/1.0"
        }

    def run(self):
        page_info = self.getBasicInfo()

        if page_info is None:
            return False


        page_wikitext = self.getWikiText(page_info["pageid"])
        if page_wikitext is None:
            return False

        # Todo: Move this to their own class (SoC)
        user_regdata = self.getUserRegDate( self.user )
        if user_regdata is None:
            return False

        page_template = self.getTemplatesFromText(page_wikitext)
        contributions = self.getContrib()

        pageImage = len( page_info["images"] ) if "images" in page_info else 0
        pageCategory = len( page_info["categories"] ) if "categories" in page_info else 0
        langLinksCount = page_info["langlinkscount"] if "langlinkscount" in page_info else 0

        return {
            "page_id": page_info["pageid"],
            "page_ns": page_info["ns"],
            "page_size": page_info["length"],
            "page_words": 400, # Todo: Create function to calc
            "pageImages": pageImage,
            "page_categories": pageCategory,
            "page_langlinks": langLinksCount,
            "pageCreatedAt": page_info["revisions"][0]["timestamp"],
            "pageCreatedBy": page_info["revisions"][0]["user"],
            "pageTemplate": page_template,
            "userRegdata": user_regdata,
            "contributions": contributions
        }

    def getBasicInfo(self):
        param = {
            "action": "query",
            "format": "json",
            "prop": "info|categories|images|langlinkscount|revisions",
            "titles": self.page,
            "utf8": 1,
            "clshow": "!hidden",
            "cllimit": "50",
            "imlimit": "50",
            "rvprop": "ids|timestamp|user|size|userid",
            "rvslots": "main",
            "rvlimit": "1",
            "rvdir": "newer"
        }

        try:
            req = requests.get(self.apiEndpoint, headers=self.header, params=param)
            res = req.json()
            return list(res["query"]["pages"].values())[0]
        except:
            return None

    def getWikiText(self, page_id):
        # Getting wiki page content
        param = {
            "action": "parse",
            "format": "json",
            "pageid": page_id,
            "prop": "text|wikitext",
            "utf8": 1
        }

        try:
            req = requests.get(self.apiEndpoint, headers=self.header, params=param)
            res = req.json()

            return res["parse"]["wikitext"]["*"]
        except:
            return None

    def getTemplatesFromText(self, wikitext):
        # Extracting number of template used in page
        # API does not help as it is returning those..
        # templates as well which are used as indirect
        p = parse(wikitext)
        temp = set()
        for i in p.filter_templates():
            temp.add( str(i.name) )

        return len(temp)

    def getUserRegDate(self, username):
        param = {
            "action": "query",
            "format": "json",
            "list": "users",
            "usprop": "registration",
            "ususers": username
        }

        r = requests.get(self.apiEndpoint, headers=self.header, params=param)
        try:
            return r.json()["query"]["users"][0]["registration"]
        except:
            return None

    def getContrib(self):
        param = {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "prop": "revisions",
            "titles": self.page,
            "rvlimit": "500",
            "rvprop": "ids|timestamp|user|size",
            "rvdir": "newer"
        }

        r = requests.get(self.apiEndpoint, headers=self.header, params=param)

        if r.status_code != 200:
            return None

        res = r.json()
        revisions = res["query"]["pages"][0]["revisions"]

        usercontrib = {}

        tempSize = None
        for i in revisions:
            curUser = i["user"]
            curSize = i["size"]

            temp = dict()
            temp["revid"], temp["timestamp"] = i["revid"], i["timestamp"]
            temp["sizediff"] = curSize if i["parentid"] == 0 else curSize - tempSize

            if curUser in usercontrib:
                usercontrib[curUser].append(temp)
            else:
                usercontrib[curUser] = []
                usercontrib[curUser].append(temp)

            tempSize = i["size"]

        return usercontrib
