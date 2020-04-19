"""Builder for Current and Pending Reports."""
import datetime as dt
import sys
import time
from argparse import RawTextHelpFormatter

import nameparser

from regolith.helpers.basehelper import SoutHelperBase, DbHelperBase
from regolith.dates import month_to_int, month_to_str_int
from regolith.fsclient import _id_key
from regolith.sorters import position_key
from regolith.tools import (
    all_docs_from_collection,
    filter_grants,
    fuzzy_retrieval,
)

ALLOWED_TYPES = ["nsf", "doe", "other"]
ALLOWED_STATI = ["invited", "accepted", "declined", "downloaded", "inprogress",
                 "submitted", "cancelled"]


def subparser(subpi):
    subpi.add_argument("name", help="pi first name space last name in quotes",
                        default=None)
    subpi.add_argument("type", help=f"{ALLOWED_TYPES}", default=None)
    subpi.add_argument("due_date", help="due date in form YYYY-MM-DD")
    subpi.add_argument("-q", "--requester",
                        help="Name of the Program officer requesting"
                        )
    subpi.add_argument("-r", "--reviewer",
                        help="name of the reviewer.  Defaults to sbillinge")
    subpi.add_argument("-s", "--status",
                        help=f"status, from {ALLOWED_STATI}. default is accepted")
    subpi.add_argument("-t", "--title",
                        help="the title of the proposal")
    return subpi

class PropRevAdderHelper(DbHelperBase):
    """Build a helper"""
    btype = "a_proprev"
    needed_dbs = ['proposalReviews']

    def construct_global_ctx(self):
        """Constructs the global context"""
        super().construct_global_ctx()
        gtx = self.gtx
        rc = self.rc
        rc.db = "test"
        rc.coll = "proposalReviews"
        gtx["proposalReviews"] = sorted(
            all_docs_from_collection(rc.client, "proposalReviews"), key=_id_key
        )
        gtx["all_docs_from_collection"] = all_docs_from_collection
        gtx["float"] = float
        gtx["str"] = str
        gtx["zip"] = zip


    def sout(self):
        person = self.rc.person
        return print(f"hello {person}")

    def db_updater(self):
        rc = self.rc
        name = nameparser.HumanName(rc.name)
        month = dt.datetime.today().month
        year = dt.datetime.today().year
        key = "{}{}_{}_{}".format(
            str(year)[-2:], month_to_str_int(month), name.last.casefold(),
            name.first.casefold().strip("."))

        coll = self.gtx["proposalReviews"]
        pdocl = dict(list(filter(lambda doc: doc["_id"] == key, coll)))
        if len(pdocl) > 0:
            sys.exit("This entry appears to already exist in the collection")
        else:
            pdoc = {}
        pdoc.update({'adequacy_of_resources': [
            'The resources available to the PI seem adequate'],
                'agency': rc.type,
                'competency_of_team': [],
                'doe_appropriateness_of_approach': [],
                'doe_reasonableness_of_budget': [],
                'doe_relevance_to_program_mission': [],
                'does_how': [],
                'does_what': '',
                'due_date': rc.due_date,
                'freewrite': [],
                'goals': [],
                'importance': [],
                'institutions': [],
                'month': 'tbd',
                'names': name.full_name,
                'nsf_broader_impacts': [],
                'nsf_create_original_transformative': [],
                'nsf_plan_good': [],
                'nsf_pot_to_advance_knowledge': [],
                'nsf_pot_to_benefit_society': [],
                'status': 'accepted',
                'summary': '',
                'year': 2020
                })

        if rc.title:
            pdoc.update({'title': rc.title})
        else:
            pdoc.update({'title': ''})
        if rc.requester:
            pdoc.update({'requester': rc.requester})
        else:
            pdoc.update({'requester': ''})
        if rc.reviewer:
            pdoc.update({'reviewer': rc.reviewer})
        else:
            pdoc.update({'reviewer': 'sbillinge'})
        if rc.status:
            if rc.status not in ALLOWED_STATI:
                raise ValueError(
                    "status should be one of {}".format(ALLOWED_STATI))
            else:
                pdoc.update({'status': rc.status})
        else:
            pdoc.update({'status': 'accepted'})

        pdoc.update({"_id": key})
        rc.client.insert_one(rc.db, rc.coll, pdoc)
#        sync_coll(file, fullpdoc)

        print("{} proposal has been added/updated in proposal reviews".format(
            rc.name))

        return


    def latex(self):
        """Render latex template"""
        for rev in self.gtx["refereeReports"]:
            outname = "{}_{}".format(_id_key(rev),rev["reviewer"])
            self.render(
                "mt.txt",
                outname + ".txt",
                trim_blocks=True,
                title=rev["title"],
                firstAuthorLastName=rev["first_author_last_name"],
                journal=rev["journal"],
                didWhat=rev["did_what"],
                didHow=rev["did_how"],
                foundWhat=rev["claimed_found_what"],
                whyImportant=rev["claimed_why_important"],
                validityAssessment=rev["validity_assessment"],
                finalAssessment=rev["final_assessment"],
                recommendation=rev["recommendation"],
                freewrite=rev["freewrite"]
            )
            if len(rev["editor_eyes_only"]) > 0:
                self.render(
                    "refreport_editor.txt",
                    outname + "_editor.txt",
                    title=rev["title"],
                    firstAuthorLastName=rev["first_author_last_name"],
                    editorEyesOnly=rev["editor_eyes_only"],
                )
