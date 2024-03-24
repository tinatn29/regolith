"""Database schemas, examples, and tools"""

import copy
import json
from pathlib import Path
from warnings import warn

from cerberus import Validator
from flatten_dict import flatten, unflatten

from .sorters import POSITION_LEVELS


SORTED_POSITION = sorted(POSITION_LEVELS.keys(), key=POSITION_LEVELS.get)
PROJECTUM_ACTIVE_STATI = ["proposed", "converged", "started"]
PROJECTUM_PAUSED_STATI = ["backburner", "paused"]
PROJECTUM_CANCELLED_STATI = ["cancelled"]
PROJECTUM_FINISHED_STATI = ["finished"]

alloweds = {
    "ACTIVITIES_TYPES": ["teaching", "research"],
    "AGENCIES": ["nsf", "doe", "other"],
    "APPOINTMENTS_TYPES": ["gra", "ss", "pd", "ug"],
    "APPOINTMENTS_STATI": ["proposed", "appointed", "finalized"],
    "COMMITTEES_TYPES": ["phdoral", "phddefense", "phdproposal", "promotion"],
    "COMMITTEES_LEVELS": ["department", "school", "university", "external"],
    "EXPENSES_STATI": ["unsubmitted", "submitted", "reimbursed", "declined"],
    "EXPENSES_TYPES": ["travel", "business"],
    "FACILITIES_TYPES": [
        "teaching",
        "research",
        "shared",
        "other",
        "teaching_wish",
        "research_wish",
    ],
    "GRANT_STATI": ["pending", "declined", "accepted", "in-prep"],
    "GRANT_ROLES": ["pi", "copi"],
    "MILESTONE_TYPES": [
        "mergedpr",
        "meeting",
        "other",
        "paper",
        "release",
        "email",
        "handin",
        "purchase",
        "approval",
        "presentation",
        "report",
        "submission",
        "decision",
        "demo",
        "skel",
    ],
    "POSITION_STATI": [
        "pi",
        "adjunct",
        "high-school",
        "undergrad",
        "ms",
        "phd",
        "postdoc",
        "visitor-supported",
        "visitor-unsupported",
        "research-associate",
    ],
    "PRESENTATION_TYPES": [
        "award",
        "colloquium",
        "contributed_oral",
        "invited",
        "keynote",
        "plenary",
        "poster",
        "seminar",
        "tutorial",
        "other",
    ],
    "PRESENTATION_STATI": [
        "in-prep",
        "submitted",
        "accepted",
        "declined",
        "cancelled",
        "postponed",
    ],
    "PROJECT_TYPES": ["ossoftware", "funded", "outreach"],
    "PROJECTUM_ACTIVE_STATI": PROJECTUM_ACTIVE_STATI,
    "PROJECTUM_PAUSED_STATI": PROJECTUM_PAUSED_STATI,
    "PROJECTUM_CANCELLED_STATI": PROJECTUM_CANCELLED_STATI,
    "PROJECTUM_FINISHED_STATI": PROJECTUM_FINISHED_STATI,
    "PROJECTUM_STATI": PROJECTUM_ACTIVE_STATI
    + PROJECTUM_PAUSED_STATI
    + PROJECTUM_CANCELLED_STATI
    + PROJECTUM_FINISHED_STATI,
    "PROPOSAL_STATI": ["pending", "declined", "accepted", "inprep", "submitted"],
    "PUBLICITY_TYPES": ["online", "article"],
    "REVIEW_STATI": [
        "invited",
        "accepted",
        "declined",
        "downloaded",
        "inprogress",
        "submitted",
        "cancelled",
    ],
    "REVIEW_RECOMMENDATIONS": [
        "reject",
        "asis",
        "smalledits",
        "diffjournal",
        "majoredits",
    ],
    "SERVICE_TYPES": ["profession", "university", "school", "department"],
    "TODO_STATI": ["started", "finished", "cancelled", "paused"],
    "OPTIONAL_KEYS_INSTITUTIONS": [
        "aka",
        "departments",
        "schools",
        "state",
        "street",
        "zip",
    ],
    # for status of kickoff, deliverable, milestones, and the projectum
}


def _update_dict_target(d, filter, new_value):
    flatd = flatten(d)
    for k, v in flatd.items():
        for filtk, filtv in filter.items():
            if filtk in k:
                if filtv == v:
                    flatd.update({k: new_value})
    return unflatten(flatd)


def insert_alloweds(doc, alloweds, key):
    for k, v in alloweds.items():
        _update_dict_target(doc, {key: k}, v)
    return doc


def load_schemas():
    here = Path(__file__).parent
    schema_file = here / "schemas.json"
    with open(schema_file, "r", encoding="utf-8") as schema_file:
        schemas = json.load(schema_file)
    schemas = insert_alloweds(schemas, alloweds, "eallowed")
    return schemas


def load_exemplars():
    here = Path(__file__).parent
    exemplars_file = here / "exemplars.json"
    with open(exemplars_file, "r", encoding="utf-8") as exemplars_file:
        exemplars = json.load(exemplars_file)
    return exemplars


# EXEMPLARS = load_exemplars()
EXEMPLARS = {
    "abstracts": {
        "_id": "Mouginot.Model",
        "coauthors": "P.P.H. Wilson",
        "email": "mouginot@wisc.edu",
        "firstname": "Baptiste",
        "institution": "University of Wisconsin-Madison",
        "lastname": "Mouginot",
        "references": "[1] B. MOUGINOT, “cyCLASS: CLASS "
        "models for Cyclus,”, Figshare, "
        "https://dx.doi.org/10.6084/"
        "m9.figshare.3468671.v2 (2016).",
        "text": "The CLASS team has developed high "
        "quality predictors based on pre-trained "
        "neural network...",
        "timestamp": "5/5/2017 13:15:59",
        "title": "Model Performance Analysis",
    },
    "assignments": {
        "_id": "hw01-rx-power",
        "category": "homework",
        "courses": ["EMCH-558-2016-S", "EMCH-758-2016-S"],
        "points": [1, 2, 3],
        "questions": ["1-9", "1-10", "1-12"],
    },
    "beamplan": {
        "_id": "test",
        "beamtime": "2020-1-XPD",
        "begin_date": "2020-01-01",
        "end_date": "2020-01-02",
        "devices": ["cryostream"],
        "exp_plan": [
            "load samples on the holder",
            "scan the holder to locate the samples",
            "take room temperature measurement of sample and the subtrate",
            "ramp down temperature to 100K",
            "ramp up, measure PDF at temperature 100K ~ 300K, 10K stepsize, 1 min exposure",
        ],
        "holder": "film holder (1 cm * 1 cm * 1 mm)",
        "measurement": "Tramp",
        "objective": "temperature ramping PDF of one WO3 film (100, 300K, 10K)",
        "pipeline": "usual",
        "prep_plan": ["films will be made by kriti"],
        "project": "20ks_wo3",
        "project_lead": "kseth",
        "samples": ["WO3 film", "glass subtrate"],
        "scanplan": ["Scanplan(bt, Tramp, 30, 80, 500, 10)"],
        "ship_plan": ["seal and ship to CU", "carry to the beamline"],
        "time": 190,
        "todo": ["todo something"],
    },
    "beamtime": {
        "_id": "2020-1-XPD",
        "begin_date": "2020-02-14",
        "begin_time": "8:00 am",
        "end_date": "2020-02-17",
        "end_time": "8:00 am",
    },
    "blog": {
        "_id": "my-vision",
        "author": "Anthony Scopatz",
        "day": 18,
        "month": "September",
        "original": "https://scopatz.com/my-vision/",
        "post": "I would like see things move forward. Deep, I know!",
        "title": "My Vision",
        "year": 2015,
    },
    "citations": [
        {
            "_id": "meurer2016sympy",
            "author": [
                "Meurer, Aaron",
                "Smith, Christopher P",
                "Paprocki, Mateusz",
                "{\\v{C}}ert{\\'\\i}k, Ond{\\v{r}}ej",
                "Rocklin, Matthew",
                "Kumar, AMiT",
                "Ivanov, Sergiu",
                "Moore, Jason K",
                "Singh, Sartaj",
                "Rathnayake, Thilina",
                "Sean Vig",
                "Brian E Granger",
                "Richard P Muller",
                "Francesco Bonazzi",
                "Harsh Gupta",
                "Shivam Vats",
                "Fredrik Johansson",
                "Fabian Pedregosa",
                "Matthew J Curry",
                "Ashutosh Saboo",
                "Isuru Fernando",
                "Sumith Kulal",
                "Robert Cimrman",
                "Anthony Scopatz",
            ],
            "doi": "10.1021/nn501591g",
            "entrytype": "article",
            "journal": "PeerJ Computer Science",
            "month": "Jan",
            "pages": "e103",
            "publisher": "PeerJ Inc. San Francisco, USA",
            "supplementary_info_urls": ["https://google.com", "https://nytimes.com"],
            "synopsis": "The description of symbolic computing in Python",
            "tags": "pdf",
            "title": "SymPy: Symbolic computing in Python",
            "volume": "4",
            "year": "2019",
        },
        {
            "_id": "meurer2016nomonth",
            "ackno": "we acknowledge useful convos with our friends",
            "author": [
                "Meurer, Aaron",
                "Anthony Scopatz",
            ],
            "doi": "tbd",
            "entrytype": "article",
            "journal": "PeerJ Computer Science",
            "facility": "nslsii, xpd",
            "month": "tbd",
            "pages": "e103",
            "publisher": "PeerJ Inc. San Francisco, USA",
            "synopsis": "A pub with month as tbd",
            "tags": "nomonth",
            "title": "SymPy: Symbolic computing in Python",
            "url": "https://doi.org/10.1021/nn501591g",
            "volume": "4",
            "year": "2017",
        },
    ],
    "contacts": {
        "_id": "afriend",
        "aka": ["A. B. Friend", "AB Friend", "Tony Friend"],
        "department": "physics",
        "email": "friend@deed.com",
        "institution": "columbiau",
        "name": "Anthony B Friend",
        "notes": ["The guy I meet for coffee sometimes"],
        "title": "Mr.",
        "month": "January",
        "year": 2020,
        "day": 15,
        "uuid": "76f2a4c7-aa63-4fa3-88b5-396b0c15d368",
    },
    "courses": {
        "_id": "EMCH-552-2016-F",
        "active": False,
        "department": "EMCH",
        "number": 552,
        "scale": [
            [0.875, "A"],
            [0.8125, "B+"],
            [0.75, "B"],
            [0.6875, "C+"],
            [0.625, "C"],
            [0.5625, "D+"],
            [0.5, "D"],
            [-1.0, "F"],
        ],
        "season": "F",
        "students": ["Human A. Person", "Human B. Person"],
        "syllabus": "emch552-2016-f-syllabus.pdf",
        "weights": {
            "class-notes": 0.15,
            "final": 0.3,
            "homework": 0.35,
            "midterm": 0.2,
        },
        "year": 2016,
    },
    "expenses": [
        {
            "_id": "test",
            "begin_date": "2018-01-01",
            "end_date": "2018-01-10",
            "expense_type": "business",
            "grant_percentages": ["50", "50"],
            "grants": ["dmref15", "SymPy-1.1"],
            "itemized_expenses": [
                {
                    "day": i,
                    "month": "Jan",
                    "year": 2018,
                    "purpose": "test",
                    "unsegregated_expense": 10 * i,
                    "segregated_expense": 0,
                    "prepaid_expense": 10.3,
                }
                for i in range(1, 11)
            ],
            "payee": "scopatz",
            "reimbursements": [
                {
                    "amount": 500,
                    "date": "tbd",
                    "submission_date": "tbd",
                    "where": "Columbia",
                },
                {
                    "amount": 1000,
                    "date": "2019-02-15",
                    "submission_date": "2019-09-05",
                    "where": "Columbia",
                },
            ],
            "project": "Cyclus",
            "overall_purpose": "testing the databallectionsse",
            "notes": "this expense was used to get the work done",
            "status": "submitted",
        },
        {
            "_id": "test2",
            "begin_date": "2019-01-01",
            "end_date": "2019-01-10",
            "expense_type": "business",
            "grant_percentages": ["100"],
            "grants": ["SymPy-1.1"],
            "itemized_expenses": [
                {
                    "day": 2,
                    "month": "Jan",
                    "year": 2019,
                    "purpose": "test",
                    "unsegregated_expense": 10,
                    "segregated_expense": 0,
                    "prepaid_expense": 10.3,
                    "currency": "USD",
                    "notes": ["this is just a test"],
                }
            ],
            "payee": "sbillinge",
            "reimbursements": [
                {
                    "amount": 100,
                    "date": "2019-09-15",
                    "submission_date": "tbd",
                    "where": "Columbia",
                },
            ],
            "project": "reimbursed expense",
            "overall_purpose": "testing",
            "notes": "some note",
            "status": "reimbursed",
        },
        {
            "_id": "test3",
            "begin_date": "2020-01-01",
            "end_date": "2020-01-10",
            "expense_type": "business",
            "grant_percentages": ["100"],
            "grants": ["SymPy-1.1"],
            "itemized_expenses": [
                {
                    "day": 3,
                    "month": "Jan",
                    "year": 2020,
                    "purpose": "test",
                    "unsegregated_expense": 10,
                    "segregated_expense": 0,
                    "prepaid_expense": 10.3,
                }
            ],
            "payee": "sbillinge",
            "reimbursements": [
                {
                    "amount": 100,
                    "date": "2020-09-15",
                    "submission_date": "tbd",
                    "where": "Columbia",
                },
            ],
            "project": "reimbursed expense",
            "overall_purpose": "more testing",
            "notes": "some other note",
            "status": "bad_status",
        },
    ],
    "grades": {
        "_id": "Human A. Person-rx-power-hw02-EMCH-758-2017-S",
        "student": "hap",
        "assignment": "2017-rx-power-hw02",
        "course": "EMCH-758-2017-S",
        "scores": [1, 1.6, 3],
    },
    "formalletters": [
        {
            "_id": "first_letter",
            "date": "2022-06-05",
            "to": {"name": "Julie Doe", "title": "lc", "postfix": "USM"},
            "copy_to": ["copied-person1", "copied-person2"],
            "from": {"name": "John Doy", "title": "Sir", "postfix": "Royalty"},
            "subject": "this letter is about this",
            "refs": ["ref 1", "ref 2"],
            "encls": ["encl 1", "encl 2"],
            "paras": [
                "first paragraph made long enough to make sure the wrapping "
                "gives the desired result and that it looks nice all around.",
                "para 2",
                "para 3",
            ],
        }
    ],
    "grants": [
        {
            "_id": "SymPy-1.1",
            "admin": "APAM",
            "amount": 3000.0,
            "alias": "sym",
            "awardnr": "NF-1234",
            "begin_day": 1,
            "begin_month": "May",
            "begin_year": 2030,
            "call_for_proposals": "https://groups.google.com/d/msg"
            "/numfocus/wPjhdm8NJiA/S8JL1_NZDQAJ",
            "end_day": 31,
            "end_month": "December",
            "end_year": 2030,
            "funder": "NumFOCUS",
            "funds_available": [
                {"date": "2020-04-01", "funds_available": 2800.00},
                {"date": "2021-01-03", "funds_available": 2100.00},
                {"date": "2020-07-21", "funds_available": 2600.00},
            ],
            "narrative": "https://docs.google.com/document/d/1nZxqoL"
            "-Ucni_aXLWmXtRDd3IWqW0mZBO65CEvDrsXZM/edit?usp"
            "=sharing",
            "program": "Small Development Grants",
            "team": [
                {
                    "institution": "University of South Carolina",
                    "name": "Anthony Scopatz",
                    "position": "pi",
                },
                {
                    "institution": "University of South Carolina",
                    "name": "Aaron Meurer",
                    "position": "researcher",
                    "admin_people": ["A. D. Ministrator"],
                },
            ],
            "status": "pending",
            "title": "SymPy 1.1 Release Support",
            "budget": [
                {
                    "begin_date": "2030-05-01",
                    "end_date": "2030-06-30",
                    "student_months": 0.5,
                    "postdoc_months": 0.0,
                    "ss_months": 1.0,
                    "amount": 1000.0,
                },
                {
                    "begin_date": "2030-07-01",
                    "end_date": "2030-09-30",
                    "student_months": 1.5,
                    "postdoc_months": 0.0,
                    "ss_months": 2.0,
                    "amount": 1000.0,
                },
                {
                    "begin_date": "2030-10-01",
                    "end_date": "2030-12-31",
                    "student_months": 3.0,
                    "postdoc_months": 0.0,
                    "ss_months": 0.0,
                    "amount": 1000.0,
                },
            ],
            "proposal_id": "SymPy-1.1",
        },
        {
            "_id": "SymPy-2.0",
            "admin": "APAM",
            "amount": 3000.0,
            "alias": "sym2.0",
            "awardnr": "NF-1234",
            "begin_day": 1,
            "begin_month": 6,
            "begin_year": 2019,
            "call_for_proposals": "https://groups.google.com/d/msg"
            "/numfocus/wPjhdm8NJiA/S8JL1_NZDQAJ",
            "end_day": 31,
            "end_month": "December",
            "end_year": 2030,
            "funder": "NumFOCUS",
            "funds_available": [
                {"date": "2020-04-01", "funds_available": 2800.00},
                {"date": "2021-01-03", "funds_available": 2100.00},
                {"date": "2020-07-21", "funds_available": 2600.00},
            ],
            "narrative": "https://docs.google.com/document/d/1nZxqoL"
            "-Ucni_aXLWmXtRDd3IWqW0mZBO65CEvDrsXZM/edit?usp"
            "=sharing",
            "program": "Small Development Grants",
            "team": [
                {
                    "institution": "University of South Carolina",
                    "name": "Anthony Scopatz",
                    "position": "pi",
                },
                {
                    "institution": "University of South Carolina",
                    "name": "Aaron Meurer",
                    "position": "researcher",
                },
            ],
            "status": "accepted",
            "title": "SymPy 2.0 Release Support",
            "budget": [
                {
                    "begin_date": "2019-06-01",
                    "end_date": "2024-12-31",
                    "student_months": 12.0,
                    "postdoc_months": 24.0,
                    "ss_months": 14.0,
                    "amount": 1500.0,
                },
                {
                    "begin_date": "2025-01-01",
                    "end_date": "2030-12-31",
                    "student_months": 12.0,
                    "postdoc_months": 24.0,
                    "ss_months": 0.0,
                    "amount": 1500.0,
                },
            ],
            "proposal_id": "SymPy-2.0",
        },
        {
            "_id": "dmref15",
            "alias": "dmref15",
            "account": "GG012345",
            "admin": "DSI",
            "amount": 982785.0,
            "awardnr": "DMR-0785462",
            "funder": "NSF",
            "grant_id": "DMREF-1534910",
            "institution": "Columbia University",
            "notes": "Designing Materials to Revolutionize and Engineer our "
            "Future (DMREF)",
            "person_months_academic": 0.0,
            "person_months_summer": 0.25,
            "program": "DMREF",
            "scope": "This grant is to develop complex modeling methods for regularizing "
            "ill-posed nanostructure inverse problems using data analytic and "
            "machine learning based approaches. This does not overlap with any "
            "other grant.",
            "team": [
                {
                    "institution": "Columbia University",
                    "name": "qdu",
                    "position": "copi",
                },
                {
                    "institution": "Columbia University",
                    "name": "dhsu",
                    "position": "copi",
                },
                {
                    "institution": "Columbia University",
                    "name": "Anthony Scopatz",
                    "position": "pi",
                    "subaward_amount": 330000.0,
                },
            ],
            "title": "DMREF: Novel, data validated, nanostructure determination "
            "methods for accelerating materials discovery",
            "budget": [
                {
                    "begin_date": "2018-05-01",
                    "end_date": "2018-09-30",
                    "student_months": 12.0,
                    "postdoc_months": 0.0,
                    "ss_months": 6.0,
                    "amount": 327595.0,
                },
                {
                    "begin_date": "2018-10-01",
                    "end_date": "2019-01-30",
                    "student_months": 8.0,
                    "postdoc_months": 0.0,
                    "ss_months": 12.0,
                    "amount": 327595.0,
                },
                {
                    "begin_date": "2019-02-01",
                    "end_date": "2019-05-01",
                    "student_months": 12.0,
                    "postdoc_months": 0.0,
                    "ss_months": 6.0,
                    "amount": 327595.0,
                },
            ],
            "proposal_id": "dmref15",
        },
        {
            "_id": "abc42",
            "alias": "abc42",
            "amount": 42000.0,
            "begin_date": "2020-06-01",
            "end_date": "2020-12-31",
            "funder": "Life",
            "program": "Metaphysical Grants",
            "team": [
                {
                    "institution": "University of Pedagogy",
                    "name": "Chief Pedagogue",
                    "position": "pi",
                },
                {
                    "institution": "University of Pedagogy",
                    "name": "Pedagogue Jr.",
                    "position": "copi",
                },
            ],
            "title": "The answer to life, the universe, and everything",
            "budget": [
                {
                    "begin_date": "2020-06-01",
                    "end_date": "2020-12-31",
                    "student_months": 0.0,
                    "postdoc_months": 0.0,
                    "ss_months": 1.0,
                    "amount": 42000.0,
                }
            ],
            "proposal_id": "abc42",
        },
        {
            "_id": "ta",
            "amount": 0.0,
            "begin_date": "2020-06-01",
            "end_date": "2020-12-31",
            "funder": "Life",
            "program": "Underground Grants",
            "team": [
                {
                    "institution": "Ministry of Magic",
                    "name": "Chief Witch",
                    "position": "pi",
                },
                {
                    "institution": "Ministry of Magic",
                    "name": "Chief Wizard",
                    "position": "copi",
                },
            ],
            "title": "Support for teaching assistants",
            "budget": [
                {
                    "begin_date": "2020-06-01",
                    "end_date": "2020-08-30",
                    "student_months": 0.0,
                    "postdoc_months": 0.0,
                    "ss_months": 0.0,
                    "amount": 0.0,
                }
            ],
        },
    ],
    "groups": {
        "_id": "ergs",
        "pi_name": "Anthony Scopatz",
        "department": "Mechanical Engineering",
        "institution": "University of South Carolina",
        "name": "ERGS",
        "aka": ["Energy Research Group Something", "Scopatz Group"],
        "website": "www.ergs.sc.edu",
        "mission_statement": """<b>ERGS</b>, or <i>Energy Research Group: 
    Scopatz</i>, is the Computational 
    <a href="http://www.me.sc.edu/nuclear/">Nuclear Engineering</a>
    research group at the 
    <a href="http://sc.edu/">University of South Carolina</a>. 
    Our focus is on uncertainty quantification & predictive modeling, nuclear 
    fuel cycle simulation, and improving nuclear engineering techniques through 
    automation.
    We are committed to open & accessible research tools and methods.""",
        "projects": """ERGS is involved in a large number of computational 
    projects. Please visit the <a href="projects.html">projects page</a> for 
    more information!
    """,
        "email": "<b>scopatz</b> <i>(AT)</i> <b>cec.sc.edu</b>",
    },
    "institutions": [
        {
            "_id": "columbiau",
            "aka": ["Columbia University", "Columbia"],
            "city": "New York",
            "country": "USA",
            "day": 30,
            "departments": {
                "physics": {
                    "name": "Department of Physics",
                    "aka": ["Dept. of Physics", "Physics"],
                },
                "chemistry": {
                    "name": "Department of Chemistry",
                    "aka": ["Chemistry", "Dept. of Chemistry"],
                },
                "apam": {
                    "name": "Department of Applied Physics " "and Applied Mathematics",
                    "aka": ["APAM"],
                },
            },
            "month": "May",
            "name": "Columbia University",
            "schools": {
                "seas": {
                    "name": "School of Engineering and " "Applied Science",
                    "aka": [
                        "SEAS",
                        "Columbia Engineering",
                        "Fu Foundation School of Engineering " "and Applied Science",
                    ],
                }
            },
            "state": "NY",
            "street": "500 W 120th St",
            "updated": "2020-05-30",
            "uuid": "avacazdraca345rfsvwre",
            "year": 2020,
            "zip": "10027",
        },
        {
            "_id": "usouthcarolina",
            "aka": ["The University of South Carolina"],
            "city": "Columbia",
            "country": "USA",
            "day": 30,
            "departments": {
                "physics": {
                    "name": "Department of Physics",
                    "aka": ["Dept. of Physics", "Physics"],
                },
                "chemistry": {
                    "name": "Department of Chemistry",
                    "aka": ["Chemistry", "Dept. of Chemistry"],
                },
                "apam": {
                    "name": "Department of Applied Physics" "and Applied Mathematics",
                    "aka": ["APAM"],
                },
                "mechanical engineering": {
                    "name": "Department of Mechanical Engineering",
                    "aka": ["Mechanical", "Dept. of Mechanical"],
                },
            },
            "month": "May",
            "name": "The University of South Carolina",
            "schools": {
                "cec": {
                    "name": "College of Engineering and" "Computing",
                    "aka": [
                        "CEC",
                        "College of Engineering and Computing",
                    ],
                }
            },
            "state": "SC",
            "street": "1716 College Street",
            "updated": "2020-06-30",
            "uuid": "4E89A0DD-19AE-45CC-BCB4-83A2D84545E3",
            "year": 2020,
            "zip": "29208",
        },
    ],
    "jobs": {
        "_id": "0004",
        "background_fields": [
            "Data Science",
            "Data Engineering",
            "Computer Engineering",
            "Computer Science",
            "Applied Mathematics",
            "Physics",
            "Nuclear Engineering",
            "Mechanical Engineering",
            "Or similar",
        ],
        "compensation": [
            "Salary and compensation will be based on prior work " "experience."
        ],
        "contact": "Please send CV or resume to Prof. Scopatz at "
        "scopatzATcec.sc.edu.",
        "day": 1,
        "description": "<p>We are seeking a dedicated individual to "
        "help to aid in ...",
        "month": "July",
        "open": False,
        "positions": ["Scientific Software Developer", "Programmer"],
        "start_date": "ASAP",
        "title": "Open Source Scientific Software Maintainer",
        "year": 2015,
    },
    "meetings": [
        {
            "_id": "grp1000-01-01",
            "actions": [
                "(Everyone) Update overdue milestones",
                "(Professor Billinge) Explore, and plan a machine learning project for DSI"
                "(Professor Billinge, Emil, Yevgeny, Songsheng) Come up with a Kaggle competition for this DSI project"
                "(Emil) Set up the slack channel for the DSI project",
            ],
            "agenda": [
                "Review actions",
                "Fargo is not free on any streaming platforms",
                "Review Airtable for deliverables and celebrate",
                "Mention diversity action initiative",
                "Songsheng's journal club presentation",
                "(Vivian and Zicheng) Finish rest of crystallography presentation next week",
                "Emil's 7th inning Yoga Stretch",
                "Crystallography talk",
                "Presentation",
            ],
            "buddies": [
                "   Jaylyn C. Umana, " "   Simon J. L. Billinge",
                "   Long Yang, " "   Emil Kjaer",
                "   Sani Harouna-Mayer," "   Akshay Choudhry",
                "   Vivian Lin, " "   Songsheng Tao",
                "   Ran Gu, " "   Adiba Ejaz",
                "   Zach Thatcher, " "   Yevgeny Rakita",
                "   Zicheng 'Taylor' Liu, " "   Eric Shen ",
                "   Hung Vuong, " "   Daniela Hikari Yano",
                "   Ahmed Shaaban, " "   Jiawei Zang",
                "   Berrak Ozer, " "   Michael Winitch",
                "   Shomik Ghose",
            ],
            "day": 1,
            "journal_club": {
                "doi": "10.1107/S2053273319005606",
                "presenter": "sbillinge",
                "link": "https://link/to/my/talk.ppt",
                "title": "what the paper was about and more",
            },
            "lead": "sbillinge",
            "minutes": [
                "Talked about eyesight and prescription lenses",
                "Professor Billinge tells everyone a Logician/Mathematician joke",
                "Mentioned pyjokes, a package in Python that lists bad jokes",
                "Jaylyn greets everyone",
                "Reviewed action items from last time",
                "Talked about fargo, and the merits (or lack thereof) of the Dakotas",
                "Celebrated finished prums",
                "Songhsheng holds journal club presentation on Machine Learning techniques",
                "Discussed Linear Classification, Gradient Descent, Perceptrons, Convolution and other ML topics",
                "Discussed how we can derive scientific meaning from ML algorithms",
                "Discussed real space versus reciprocal space",
                "Finished journal club, had to postpone Akshay's presentation, and the Yoga session to next week",
            ],
            "month": 1,
            "place": "Mudd 1106",
            "presentation": {
                "title": "PDF Distance Extraction",
                "link": "2007ac_grpmtg",
                "presenter": "sbillinge",
            },
            "scribe": "sbillinge",
            "time": "0",
            "updated": "2020-07-31 23:27:50.764475",
            "uuid": "3fbee8d9-e283-48e7-948f-eecfc2a123b7",
            "year": 1000,
        },
        {
            "_id": "grp2020-07-31",
            "actions": [
                "(Everyone) Update overdue milestones",
                "(Professor Billinge) Explore, and plan a machine learning project for DSI"
                "(Professor Billinge, Emil, Yevgeny, Songsheng) Come up with a Kaggle competition for this DSI project"
                "(Emil) Set up the slack channel for the DSI project",
            ],
            "agenda": [
                "Review actions",
                "Fargo is not free on any streaming platforms",
                "Review Airtable for deliverables and celebrate",
                "Mention diversity action initiative",
                "Songsheng's journal club presentation",
                "(Vivian and Zicheng) Finish rest of crystallography presentation next week",
                "Emil's 7th inning Yoga Stretch",
                "Crystallography talk",
                "Presentation",
            ],
            "buddies": [
                "   Jaylyn C. Umana, " "   Simon J. L. Billinge",
                "   Long Yang, " "   Emil Kjaer",
                "   Sani Harouna-Mayer," "   Akshay Choudhry",
                "   Vivian Lin, " "   Songsheng Tao",
                "   Ran Gu, " "   Adiba Ejaz",
                "   Zach Thatcher, " "   Yevgeny Rakita",
                "   Zicheng 'Taylor' Liu, " "   Eric Shen ",
                "   Hung Vuong, " "   Daniela Hikari Yano",
                "   Ahmed Shaaban, " "   Jiawei Zang",
                "   Berrak Ozer, " "   Michael Winitch",
                "   Shomik Ghose",
            ],
            "day": 1,
            "journal_club": {
                "doi": "10.1107/S2053273319005606",
                "link": "http://myslides.com/link/to/2007ac_grpmtg",
                "presenter": "not_a_valid_group_id",
            },
            "lead": "sbillinge",
            "minutes": [
                "Talked about eyesight and prescription lenses",
                "Professor Billinge tells everyone a Logician/Mathematician joke",
                "Mentioned pyjokes, a package in Python that lists bad jokes",
                "Jaylyn greets everyone",
                "Reviewed action items from last time",
                "Talked about fargo, and the merits (or lack thereof) of the Dakotas",
                "Celebrated finished prums",
                "Songhsheng holds journal club presentation on Machine Learning techniques",
                "Discussed Linear Classification, Gradient Descent, Perceptrons, Convolution and other ML topics",
                "Discussed how we can derive scientific meaning from ML algorithms",
                "Discussed real space versus reciprocal space",
                "Finished journal club, had to postpone Akshay's presentation, and the Yoga session to next week",
            ],
            "month": 1,
            "place": "Mudd 1106",
            "presentation": {
                "title": "PDF Distance Extraction",
                "link": "2007ac_grpmtg",
                "presenter": "not_a_valid_group_id",
            },
            "scribe": "sbillinge",
            "time": "0",
            "updated": "2020-07-31 23:27:50.764475",
            "uuid": "3fbee8d9-e283-48e7-948f-eecfc2a123b7",
            "year": 7000,
        },
    ],
    "news": {
        "_id": "56b4eb6d421aa921504ef2a9",
        "author": "Anthony Scopatz",
        "body": "Dr. Robert Flanagan joined ERGS as a post-doctoral " "scholar.",
        "day": 1,
        "month": "February",
        "year": 2016,
    },
    "people": [
        {
            "_id": "scopatz",
            "aka": [
                "Scopatz",
                "Scopatz, A",
                "Scopatz, A.",
                "Scopatz, A M",
                "Anthony Michael Scopatz",
            ],
            "avatar": "https://avatars1.githubusercontent.com/u/320553?v" "=3&s=200",
            "appointments": {
                "f19": {
                    "begin_year": 2019,
                    "begin_month": 2,
                    "begin_day": 1,
                    "end_year": 2019,
                    "end_month": 3,
                    "end_day": 31,
                    "grant": "dmref15",
                    "type": "pd",
                    "loading": 0.75,
                    "status": "finalized",
                    "notes": ["forgetmenot"],
                },
                "s20": {
                    "begin_date": "2020-01-01",
                    "end_date": "2020-05-15",
                    "grant": "sym",
                    "type": "pd",
                    "loading": 1.0,
                    "status": "finalized",
                    "notes": ["fully appointed", "outdated grant"],
                },
                "ss20": {
                    "begin_date": "2020-06-01",
                    "end_date": "2020-08-31",
                    "grant": "abc42",
                    "type": "ss",
                    "loading": 0.8,
                    "status": "proposed",
                    "notes": [],
                },
                "ss21": {
                    "begin_date": "2020-09-01",
                    "end_date": "2021-08-31",
                    "grant": "future_grant",
                    "type": "ss",
                    "loading": 1.0,
                    "status": "proposed",
                    "notes": [],
                },
            },
            "bio": "Anthony Scopatz is currently an Assistant Professor",
            "bios": [
                "Anthony Scopatz is currently an Assistant Professor but will go on to do great things"
            ],
            "committees": [
                {
                    "name": "Heather Stanford",
                    "type": "phdoral",
                    "year": 2020,
                    "month": 3,
                    "day": 1,
                    "level": "department",
                    "unit": "apam",
                },
                {
                    "name": "Heather Stanford",
                    "type": "promotion",
                    "year": 2020,
                    "month": 3,
                    "day": 1,
                    "level": "school",
                    "unit": "seas",
                },
                {
                    "name": "Heather Stanford",
                    "type": "phddefense",
                    "year": 2020,
                    "month": 3,
                    "day": 1,
                    "notes": "something else to remember about it, not published",
                    "level": "external",
                    "unit": "U Denmark",
                },
                {
                    "name": "Heather Stanford",
                    "type": "promotion",
                    "year": 2020,
                    "month": 3,
                    "day": 1,
                    "unit": "columbiau",
                    "level": "university",
                },
            ],
            "education": [
                {
                    "advisor": "scopatz",
                    "begin_year": 2008,
                    "degree": "Ph.D. Mechanical Engineering, "
                    "Nuclear and Radiation Engineering "
                    "Program",
                    "end_year": 2011,
                    "group": "ergs",
                    "institution": "The University of Texas at Austin",
                    "department": "apam",
                    "location": "Austin, TX",
                    "other": [
                        "Adviser: Erich A. Schneider",
                        "Dissertation: Essential Physics for Fuel Cycle "
                        "Modeling & Analysis",
                    ],
                },
                {
                    "begin_year": 2006,
                    "degree": "M.S.E. Mechanical Engineering, Nuclear and "
                    "Radiation Engineering Program",
                    "end_year": 2007,
                    "institution": "The University of Texas at Austin",
                    "location": "Austin, TX",
                    "other": [
                        "Adviser: Erich A. Schneider",
                        "Thesis: Recyclable Uranium Options under the Global "
                        "Nuclear Energy Partnership",
                    ],
                },
                {
                    "begin_year": 2002,
                    "begin_month": "Sep",
                    "begin_day": 1,
                    "degree": "B.S. Physics",
                    "end_year": 2006,
                    "end_month": 5,
                    "end_day": 20,
                    "institution": "University of California, Santa Barbara",
                    "location": "Santa Barbara, CA",
                    "other": [
                        "Graduated with a Major in Physics and a Minor in "
                        "Mathematics"
                    ],
                },
                {
                    "begin_year": 2008,
                    "degree": "ongoing",
                    "group": "life",
                    "institution": "solar system",
                    "department": "earth",
                    "location": "land, mostly",
                },
            ],
            "email": "scopatz@cec.sc.edu",
            "employment": [
                {
                    "advisor": "scopatz",
                    "begin_year": 2015,
                    "coworkers": ["afriend"],
                    "group": "ergs",
                    "status": "ms",
                    "location": "Columbia, SC",
                    "organization": "The University of South Carolina",
                    "other": [
                        "Cyclus: An agent-based, discrete time nuclear fuel "
                        "cycle simulator.",
                        "PyNE: The Nuclear Engineering Toolkit.",
                        "Website: http://www.ergs.sc.edu/",
                    ],
                    "permanent": True,
                    "position": "assistant professor",
                    "position_full": "Assistant Professor, Mechanical Engineering "
                    "Department",
                },
                {
                    "begin_year": 2013,
                    "begin_month": "Jun",
                    "begin_day": 1,
                    "end_year": 2015,
                    "end_month": 3,
                    "end_day": 15,
                    "advisor": "scopatz",
                    "status": "undergrad",
                    "location": "Madison, WI",
                    "organization": "CNERG, The University of " "Wisconsin-Madison",
                    "department": "Physics",
                    "other": [
                        "Cyclus: An agent-based, discrete time nuclear fuel "
                        "cycle simulator.",
                        "PyNE: The Nuclear Engineering Toolkit.",
                        "Website: https://cnerg.github.io/",
                    ],
                    "position": "associate scientist",
                    "position_full": "Associate Scientist, Engineering Physics "
                    "Department",
                },
                {
                    "begin_day": 1,
                    "begin_month": "Nov",
                    "begin_year": 2011,
                    "end_month": "May",
                    "end_year": 2013,
                    "location": "Chicago, IL",
                    "organization": "The FLASH Center, The University of " "Chicago",
                    "other": [
                        "NIF: Simulation of magnetic field generation from "
                        "neutral plasmas using FLASH.",
                        "CosmoB: Simulation of magnetic field generation "
                        "from neutral plasmas using FLASH.",
                        "FLASH4: High-energy density physics capabilities "
                        "and utilities.",
                        "Simulated Diagnostics: Schlieren, shadowgraphy, "
                        "Langmuir probes, etc. from FLASH.",
                        "OpacPlot: HDF5-based equation of state and opacity "
                        "file format.",
                        "Website: http://flash.uchicago.edu/site/",
                    ],
                    "position": "post-doctoral scholar",
                    "position_full": "Research Scientist, Postdoctoral Scholar",
                    "status": "pi",
                },
                {
                    "begin_date": "2000-01-01",
                    "end_date": "2001-12-31",
                    "location": "Chicago, IL",
                    "organization": "Google",
                    "other": [],
                    "position": "janitor",
                    "not_in_cv": True,
                },
            ],
            "funding": [
                {
                    "name": "Omega Laser User's Group Travel Award",
                    "value": 1100,
                    "year": 2013,
                },
                {"name": "NIF User's Group Travel Award", "value": 1150, "year": 2013},
            ],
            "google_scholar_url": "https://scholar.google.com/citations?user=dRm8f",
            "github_id": "ascopatz",
            "hindex": [
                {
                    "h": 25,
                    "h_last_five": 46,
                    "citations": 19837,
                    "citations_last_five": 9419,
                    "origin": "Google Scholar",
                    "since": 1991,
                    "year": 2020,
                    "month": 2,
                    "day": 19,
                }
            ],
            "home_address": {
                "street": "123 Wallabe Ln",
                "city": "The big apple",
                "state": "plasma",
                "zip": "007",
            },
            "initials": "AMS",
            "membership": [
                {
                    "begin_year": 2006,
                    "organization": "American Nuclear Society",
                    "position": "Member",
                },
                {
                    "begin_year": 2013,
                    "organization": "Python Software Foundation",
                    "position": "Fellow",
                },
            ],
            "name": "Anthony Scopatz",
            "orcid_id": "0000-0002-9432-4248",
            "position": "professor",
            "research_focus_areas": [
                {
                    "begin_year": 2010,
                    "description": "software applied to nuclear "
                    "engineering and life",
                }
            ],
            "service": [
                {
                    "name": "International Steering Committee",
                    "role": "chair",
                    "type": "profession",
                    "year": 2020,
                    "month": 3,
                    "notes": ["something"],
                },
                {
                    "name": "National Steering Committee",
                    "type": "profession",
                    "begin_year": 2018,
                    "end_year": 2021,
                    "notes": "something",
                },
            ],
            "skills": [
                {
                    "category": "Programming Languages",
                    "level": "expert",
                    "name": "Python",
                },
                {
                    "category": "Programming Languages",
                    "level": "expert",
                    "name": "Cython",
                },
            ],
            "teaching": [
                {
                    "course": "EMCH 552: Intro to Nuclear Engineering",
                    "courseid": "EMCH 552",
                    "description": "This course is an introduction to nuclear "
                    "physics.",
                    "enrollment": "tbd",
                    "month": "August",
                    "organization": "University of South Carolina",
                    "position": "professor",
                    "semester": "Spring",
                    "syllabus": "https://drive.google.com/open?id"
                    "=0BxUpd34yizZreDBCMEJNY2FUbnc",
                    "year": 2017,
                },
                {
                    "course": "EMCH 558/758: Reactor Power Systems",
                    "courseid": "EMCH 558",
                    "description": "This course covers conventional " "reactors.",
                    "enrollment": 28,
                    "evaluation": {
                        "response_rate": 66.76,
                        "amount_learned": 3.5,
                        "appropriateness_workload": 3.15,
                        "course_overall": 3.67,
                        "fairness_grading": 3.54,
                        "organization": 3.25,
                        "classroom_delivery": 4,
                        "approachability": 4.3,
                        "instructor_overall": 3.5,
                        "comments": ["super duper", "dandy"],
                    },
                    "month": "January",
                    "organization": "University of South Carolina",
                    "position": "professor",
                    "syllabus": "https://docs.google.com/document/d"
                    "/1uMAx_KFZK9ugYyF6wWtLLWgITVhaTBkAf8"
                    "-PxiboYdM/edit?usp=sharing",
                    "year": 2017,
                },
            ],
            "title": "Dr.",
        },
        {
            "_id": "sbillinge",
            "active": True,
            "activities": [
                {
                    "type": "teaching",
                    "name": "course development",
                    "year": 2018,
                    "other": "Developed a new course for Materials Science",
                }
            ],
            "aka": [
                "Billinge",
            ],
            "avatar": "https://avatars1.githubusercontent.com/u/320553?v" "=3&s=200",
            "bio": "Simon teaches and does research",
            "committees": [
                {
                    "name": "Same Old",
                    "type": "phddefense",
                    "year": 2018,
                    "unit": "Materials Science",
                    "level": "department",
                    "notes": "something",
                }
            ],
            "education": [
                {
                    "begin_year": 2008,
                    "degree": "Ph.D. Mechanical Engineering, "
                    "Nuclear and Radiation Engineering "
                    "Program",
                    "end_year": 2011,
                    "group": "ergs",
                    "advisor": "scopatz",
                    "institution": "The University of Texas at Austin",
                    "department": "apam",
                    "location": "Austin, TX",
                    "other": [
                        "Adviser: Erich A. Schneider",
                        "Dissertation: Essential Physics for Fuel Cycle "
                        "Modeling & Analysis",
                    ],
                },
            ],
            "email": "sb2896@columbia.edu",
            "employment": [
                {
                    "begin_year": 2015,
                    "group": "ergs",
                    "location": "Columbia, SC",
                    "organization": "The University of South Carolina",
                    "status": "phd",
                    "advisor": "scopatz",
                    "other": [
                        "Cyclus: An agent-based, discrete time nuclear fuel "
                        "cycle simulator.",
                        "PyNE: The Nuclear Engineering Toolkit.",
                        "Website: http://www.ergs.sc.edu/",
                    ],
                    "position": "assistant professor",
                },
            ],
            "facilities": [
                {
                    "type": "other",
                    "name": "Shared {Habanero} compute cluster",
                    "begin_year": 2015,
                },
                {
                    "type": "research_wish",
                    "name": "Shared access to wet lab",
                    "begin_year": 2015,
                },
                {"type": "teaching", "name": "Courseworks2", "begin_year": 2017},
                {
                    "type": "teaching_wish",
                    "name": "nothing right now",
                    "begin_year": 2019,
                },
                {"type": "research", "name": "I don't have one", "begin_year": 2008},
            ],
            "funding": [
                {
                    "name": "Omega Laser User's Group Travel Award",
                    "value": 1100,
                    "year": 2013,
                },
                {"name": "NIF User's Group Travel Award", "value": 1150, "year": 2013},
            ],
            "google_scholar_url": "https://scholar.google.com/citations?user=dRm8f",
            "grp_mtg_active": True,
            "hindex": [
                {
                    "h": 65,
                    "h_last_five": 43,
                    "citations": 17890,
                    "citations_last_five": 8817,
                    "origin": "Google Scholar",
                    "since": 1991,
                    "year": 2019,
                    "month": "May",
                    "day": 12,
                }
            ],
            "office": "1105 Seely W. Mudd Building (inner office)",
            "home_address": {
                "street": "123 Wallabe Ln",
                "city": "The big apple",
                "state": "plasma",
                "zip": "007",
            },
            "initials": "SJLB",
            "linkedin_url": "https://scholar.google.com/citations?hl=en&user=PAJ",
            "membership": [
                {
                    "begin_year": 2006,
                    "organization": "American Nuclear Society",
                    "position": "Member",
                },
            ],
            "miscellaneous": {
                "metrics_for_success": [
                    "publications(quality, quantity)",
                    "invite talks",
                    "funding",
                    "citations",
                ],
            },
            "name": "Simon J. L. Billinge",
            "orcid_id": "0000-0002-9432-4248",
            "position": "professor",
            "publicity": [
                {
                    "type": "online",
                    "publication": "Brookhaven National Laboratory Web Story",
                    "topic": "LDRD Provenance project",
                    "title": "An awesome project and well worth the money",
                    "day": 24,
                    "month": "Jul",
                    "year": 2019,
                    "date": "2019-07-24",
                    "grant": "bnlldrd18",
                    "url": "http://www.google.com",
                },
            ],
            "research_focus_areas": [
                {
                    "begin_year": 2010,
                    "description": "software applied to materials "
                    "engineering and life",
                }
            ],
            "service": [
                {
                    "type": "profession",
                    "name": "Master of Ceremonies and Organizer Brown University "
                    '"Chemistry: Believe it or Not" public chemistry '
                    "demonstration",
                    "year": 2017,
                    "month": "August",
                },
                {
                    "type": "department",
                    "name": "Applied Physics program committee",
                    "begin_date": "2018-01-01",
                    "end_date": "2018-01-01",
                },
                {
                    "type": "school",
                    "name": "Ad hoc tenure committee",
                    "date": "2017-06-01",
                    "notes": "Albert Einstein",
                },
                {
                    "type": "profession",
                    "name": "Co-organizer JUAMI",
                    "year": 2017,
                    "month": 12,
                    "role": "co-organizer",
                    "other": ["great way to meet people"],
                },
            ],
            "skills": [
                {
                    "category": "Programming Languages",
                    "level": "expert",
                    "name": "Python",
                },
            ],
            "teaching": [
                {
                    "course": "MSAE-3010: Introduction to Materials Science",
                    "courseid": "f16-3010",
                    "description": "This course is an introduction to nuclear "
                    "physics.",
                    "enrollment": 18,
                    "evaluation": {
                        "response_rate": 58.33,
                        "amount_learned": 4.57,
                        "appropriateness_workload": 4.29,
                        "fairness_grading": 4.57,
                        "course_overall": 4.43,
                        "organization": 4.0,
                        "classroom_delivery": 4.29,
                        "approachability": 4.86,
                        "instructor_overall": 4.43,
                        "comments": [
                            "Great teacher but disorganized",
                            "Wears pink pants.  Why?",
                        ],
                    },
                    "month": "August",
                    "organization": "Columbia University",
                    "position": "professor",
                    "semester": "Fall",
                    "syllabus": "https://drive.google.com/open?id"
                    "=0BxUpd34yizZreDBCMEJNY2FUbnc",
                    "year": 2016,
                },
                {
                    "course": "MSAE-3010: Introduction to Materials Science",
                    "courseid": "f17-3010",
                    "description": "This course is an introduction to nuclear "
                    "physics.",
                    "enrollment": 18,
                    "evaluation": {
                        "response_rate": 58.33,
                        "amount_learned": 4.57,
                        "appropriateness_workload": 4.29,
                        "fairness_grading": 4.57,
                        "course_overall": 4.43,
                        "organization": 4.0,
                        "classroom_delivery": 4.29,
                        "approachability": 4.86,
                        "instructor_overall": 4.43,
                        "comments": [
                            "Great teacher but disorganized",
                            "Wears pink pants.  Why?",
                        ],
                    },
                    "month": "August",
                    "organization": "Columbia University",
                    "position": "professor",
                    "semester": "Fall",
                    "syllabus": "https://drive.google.com/open?id"
                    "=0BxUpd34yizZreDBCMEJNY2FUbnc",
                    "year": 2017,
                },
                {
                    "course": "MSAE-3010: Introduction to Materials Science",
                    "courseid": "s18-3010",
                    "description": "This course is an introduction to nuclear "
                    "physics.",
                    "enrollment": 18,
                    "evaluation": {
                        "response_rate": 58.33,
                        "amount_learned": 4.57,
                        "appropriateness_workload": 4.29,
                        "fairness_grading": 4.57,
                        "course_overall": 4.43,
                        "organization": 4.0,
                        "classroom_delivery": 4.29,
                        "approachability": 4.86,
                        "instructor_overall": 4.43,
                        "comments": [
                            "Great teacher but disorganized",
                            "Wears pink pants.  Why?",
                        ],
                    },
                    "month": "Jan",
                    "organization": "Columbia University",
                    "position": "professor",
                    "semester": "Spring",
                    "syllabus": "https://drive.google.com/open?id"
                    "=0BxUpd34yizZreDBCMEJNY2FUbnc",
                    "year": 2018,
                },
                {
                    "course": "MSAE-3010: Introduction to Materials Science",
                    "courseid": "s17-3010",
                    "description": "This course is an introduction to nuclear "
                    "physics.",
                    "enrollment": 18,
                    "evaluation": {
                        "response_rate": 58.33,
                        "amount_learned": 4.57,
                        "appropriateness_workload": 4.29,
                        "fairness_grading": 4.57,
                        "course_overall": 4.43,
                        "organization": 4.0,
                        "classroom_delivery": 4.29,
                        "approachability": 4.86,
                        "instructor_overall": 4.43,
                        "comments": [
                            "Great teacher but disorganized",
                            "Wears pink pants.  Why?",
                        ],
                    },
                    "month": "Jan",
                    "organization": "Columbia University",
                    "position": "professor",
                    "semester": "Spring",
                    "syllabus": "https://drive.google.com/open?id"
                    "=0BxUpd34yizZreDBCMEJNY2FUbnc",
                    "year": 2017,
                },
                {
                    "course": "MSAE-3010: Introduction to Materials Science",
                    "courseid": "s19-3010",
                    "description": "This course is an introduction to nuclear "
                    "physics.",
                    "enrollment": 18,
                    "month": "Jan",
                    "organization": "Columbia University",
                    "position": "professor",
                    "semester": "Spring",
                    "syllabus": "https://drive.google.com/open?id"
                    "=0BxUpd34yizZreDBCMEJNY2FUbnc",
                    "year": 2019,
                },
                {
                    "course": "MSAE-3010: Introduction to Materials Science",
                    "courseid": "f18-3010",
                    "description": "This course is an introduction to nuclear "
                    "physics.",
                    "enrollment": 18,
                    "month": "August",
                    "organization": "Columbia University",
                    "position": "professor",
                    "semester": "Fall",
                    "syllabus": "https://drive.google.com/open?id"
                    "=0BxUpd34yizZreDBCMEJNY2FUbnc",
                    "year": 2018,
                },
                {
                    "course": "MSAE-3010: Introduction to Materials Science",
                    "courseid": "f19-3010",
                    "description": "This course is an introduction to nuclear "
                    "physics.",
                    "month": "August",
                    "organization": "Columbia University",
                    "position": "professor",
                    "semester": "Fall",
                    "syllabus": "https://drive.google.com/open?id"
                    "=0BxUpd34yizZreDBCMEJNY2FUbnc",
                    "year": 2019,
                },
            ],
            "title": "Dr.",
        },
        {
            "_id": "abeing",
            "active": False,
            "aka": ["being", "human", "person"],
            "avatar": "https://xkcd.com/1221/",
            "bio": "Abstract Being is an exemplar human existence",
            "education": [
                {
                    "degree": "bachelors",
                    "institution": "University of Laughs",
                    "begin_year": 2010,
                },
            ],
            "employment": [
                {
                    "group": "bg",
                    "begin_date": "2015-06-01",
                    "end_date": "2015-08-31",
                    "organization": "columbiau",
                    "position": "intern",
                },
                {
                    "group": "agroup",
                    "begin_date": "2020-01-01",
                    "end_date": "2030-12-31",
                    "organization": "usouthcarolina",
                    "position": "intern",
                },
                {
                    "group": "ergs",
                    "begin_date": "2010-06-01",
                    "end_date": "2012-08-31",
                    "organization": "columbiau",
                    "position": "intern",
                },
                {
                    "group": "bg",
                    "begin_date": "2017-06-01",
                    "end_date": "2019-08-31",
                    "organization": "columbiau",
                    "position": "intern",
                },
            ],
            "position": "intern",
            "name": "Abstract Being",
        },
    ],
    "presentations": [
        {
            "_id": "18sb_this_and_that",
            "abstract": "We pulled apart graphite with tape",
            "authors": ["scopatz", "afriend"],
            "begin_year": 2018,
            "begin_month": 5,
            "begin_day": 22,
            "department": "apam",
            "institution": "columbiau",
            "location": "Upton NY",
            "meeting_name": "Meeting to check flexibility on dates",
            "notes": [
                "We hope the weather will be sunny",
                "if the weather is nice we will go to the " "beach",
            ],
            "presentation_url": "http://github.com/blob/my_talk.pdf",
            "project": "18sob_clustermining",
            "status": "accepted",
            "title": "Graphitic Dephenestration",
            "type": "award",
            "webinar": False,
        },
        {
            "_id": "18sb_nslsii",
            "abstract": "We pulled apart graphite with tape",
            "authors": ["scopatz"],
            "begin_year": 2018,
            "begin_month": 5,
            "begin_day": 22,
            "department": "apam",
            "end_year": 2018,
            "end_month": 5,
            "end_day": 22,
            "institution": "columbiau",
            "location": "Upton NY",
            "meeting_name": "2018 NSLS-II and CFN Users Meeting",
            "notes": [
                "We hope the weather will be sunny",
                "if the weather is nice we will go to the " "beach",
            ],
            "project": "18sob_clustermining",
            "status": "accepted",
            "title": "ClusterMining: extracting core structures of "
            "metallic nanoparticles from the atomic pair "
            "distribution function",
            "type": "poster",
        },
        {
            "_id": "18sb04_kentstate",
            "abstract": "We made the case for local structure",
            "authors": ["scopatz"],
            "begin_year": 2018,
            "begin_month": "May",
            "begin_day": 22,
            "department": "physics",
            "end_year": 2018,
            "end_month": 5,
            "end_day": 22,
            "institution": "columbiau",
            "notes": ["what a week!"],
            "project": "18kj_conservation",
            "status": "accepted",
            "title": "Nanostructure challenges and successes from "
            "16th Century warships to 21st Century energy",
            "type": "colloquium",
            "webinar": True,
        },
    ],
    "projecta": [
        {
            "_id": "sb_firstprojectum",
            "begin_date": "2020-04-28",
            "collaborators": ["aeinstein", "pdirac"],
            "deliverable": {
                "audience": ["beginning grad in chemistry"],
                "due_date": "2021-05-05",
                "success_def": "audience is happy",
                "scope": [
                    "UCs that are supported or some other scope description "
                    "if it is software",
                    "sketch of science story if it is paper",
                ],
                "platform": "description of how and where the audience will access "
                "the deliverable.  Journal if it is a paper",
                "roll_out": [
                    "steps that the audience will take to access and interact with "
                    "the deliverable",
                    "not needed for paper submissions",
                ],
                "notes": ["deliverable note"],
                "status": "proposed",
            },
            "description": "My first projectum",
            "grants": "SymPy-1.1",
            "group_members": ["ascopatz"],
            "kickoff": {
                "date": "2020-05-05",
                "due_date": "2020-05-06",
                "end_date": "2020-05-07",
                "name": "Kick off meeting",
                "objective": "introduce project to the lead",
                "audience": ["lead", "pi", "group_members"],
                "notes": ["kickoff note"],
                "status": "finished",
            },
            "lead": "ascopatz",
            "log_url": "https://docs.google.com/document/d/1YC_wtW5Q",
            "milestones": [
                {
                    "due_date": "2020-05-20",
                    "name": "Project lead presentation",
                    "notes": ["do background reading", "understand math"],
                    "tasks": ["1saefadf-wdaagea2"],
                    "objective": "lead presents background reading and "
                    "initial project plan",
                    "audience": ["lead", "pi", "group_members"],
                    "status": "proposed",
                    "type": "meeting",
                    "progress": {
                        "text": "The samples have been synthesized and places in the sample cupboard. "
                        "They turned out well and are blue as expected",
                        "figure": [
                            "token that dereferences a figure or image in group local storage db"
                        ],
                        "slides_urls": [
                            "url to slides describing the development, e.g. Google slides url"
                        ],
                    },
                    "uuid": "milestone_uuid_sb1",
                },
                {
                    "due_date": "2020-05-27",
                    "name": "planning meeting",
                    "objective": "develop a detailed plan with dates",
                    "audience": ["lead", "pi", "group_members"],
                    "status": "proposed",
                    "type": "mergedpr",
                    "uuid": "milestone_uuid_sb1_2",
                },
            ],
            "name": "First Projectum",
            "pi_id": "scopatz",
            "supplementary_info_urls": ["https://google.com", "https://nytimes.com"],
            "status": "started",
            "other_urls": ["https://docs.google.com/document/d/analysis"],
            "product_url": "https://docs.google.com/document/d/manuscript",
        },
        {
            "_id": "ab_inactive",
            "lead": "abeing",
            "begin_date": "2020-05-03",
            "status": "backburner",
            "grants": "dmref15",
            "description": "a prum that has various inactive states in milestones and overall",
            "deliverable": {"due_date": "2021-05-03", "status": "paused"},
            "kickoff": {
                "due_date": "2021-05-03",
                "name": "Kickoff",
                "status": "backburner",
                "type": "meeting",
            },
            "milestones": [
                {
                    "due_date": "2021-05-03",
                    "name": "Milestone",
                    "status": "converged",
                    "uuid": "milestone_uuid_inactive",
                }
            ],
        },
        {
            "_id": "pl_firstprojectum",
            "lead": "pliu",
            "status": "finished",
            "begin_date": "2020-07-25",
            "end_date": "2020-07-27",
            "deliverable": {"due_date": "2021-08-26", "status": "finished"},
            "kickoff": {
                "due_date": "2021-08-03",
                "name": "Kickoff",
                "status": "backburner",
            },
            "milestones": [
                {
                    "due_date": "2021-08-03",
                    "name": "Milestone",
                    "status": "converged",
                    "uuid": "milestone_uuid_pl1",
                }
            ],
        },
        {
            "_id": "pl_secondprojectum",
            "lead": "pliu",
            "status": "proposed",
            "begin_date": "2020-07-25",
            "deliverable": {"due_date": "2021-08-26", "status": "finished"},
            "kickoff": {
                "due_date": "2021-08-03",
                "name": "Kickoff",
                "status": "backburner",
            },
            "milestones": [
                {
                    "due_date": "2021-08-03",
                    "name": "Milestone",
                    "status": "converged",
                    "uuid": "milestone_uuid_pl2",
                }
            ],
        },
        {
            "_id": "pl_thirdprojectum",
            "lead": "pliu",
            "status": "backburner",
            "begin_date": "2020-07-25",
            "deliverable": {"due_date": "2021-08-26", "status": "finished"},
            "kickoff": {
                "due_date": "2021-08-03",
                "name": "Kickoff",
                "status": "backburner",
            },
            "milestones": [
                {
                    "due_date": "2021-08-03",
                    "name": "Milestone",
                    "status": "converged",
                    "uuid": "milestone_uuid_pl3",
                }
            ],
        },
    ],
    "projects": {
        "_id": "Cyclus",
        "name": "Cyclus",
        "description": "Agent-Based Nuclear Fuel Cycle Simulator",
        "group": "ergs",
        "highlights": [
            {"year": 2020, "month": 5, "description": "high profile pub in Nature"}
        ],
        "logo": "http://fuelcycle.org/_static/big_c.png",
        "other": [
            "Discrete facilities with discrete material transactions",
            "Low barrier to entry, rapid payback to adoption",
        ],
        "repo": "https://github.com/cyclus/cyclus/",
        "team": [
            {
                "begin_month": "June",
                "begin_year": 2013,
                "end_month": "July",
                "end_year": 2015,
                "name": "Anthony Scopatz",
                "position": "Project Lead",
            }
        ],
        "type": "funded",
        "website": "http://fuelcycle.org/",
        "grant": "dmref15",
    },
    "proposalReviews": [
        {
            "_id": "1906doeExample",
            "adequacy_of_resources": [
                "The resources available to the PI seem adequate"
            ],
            "agency": "doe",
            "competency_of_team": ["super competent!"],
            "doe_appropriateness_of_approach": [
                "The proposed approach is highly innovative"
            ],
            "doe_reasonableness_of_budget": ["They could do it with half the money"],
            "doe_relevance_to_program_mission": ["super relevant"],
            "does_how": [
                "they will find the cause of Malaria",
                "when they find it they will determine a cure",
            ],
            "due_date": "2020-04-10",
            "does_what": "Find a cure for Malaria",
            "freewrite": [
                "I can put extra things here, such as special instructions from the",
                "program officer",
            ],
            "goals": [
                "The goals of the proposal are to put together a team to find a cure"
                "for Malaria, and then to find it"
            ],
            "importance": ["save lives", "lift people from poverty"],
            "institutions": "columbiau",
            "month": "May",
            "names": ["B. Cause", "A.N. Effect"],
            "nsf_broader_impacts": [],
            "nsf_create_original_transformative": [],
            "nsf_plan_good": [],
            "nsf_pot_to_advance_knowledge": [],
            "nsf_pot_to_benefit_society": [],
            "requester": "Lane Wilson",
            "reviewer": "sbillinge",
            "status": "submitted",
            "summary": "dynamite proposal",
            "title": "A stunning new way to cure Malaria",
            "year": 2019,
        },
        {
            "_id": "1906nsfExample",
            "adequacy_of_resources": [
                "The resources available to the PI seem adequate"
            ],
            "agency": "nsf",
            "competency_of_team": ["super competent!"],
            "doe_appropriateness_of_approach": [],
            "doe_reasonableness_of_budget": [],
            "doe_relevance_to_program_mission": [],
            "does_how": [
                "they will find the cause of Poverty",
                "when they find it they will determine a cure",
            ],
            "does_what": "Find a cure for Poverty",
            "due_date": "2020-04-10",
            "freewrite": "I can put extra things here, such as special instructions from the",
            "goals": [
                "The goals of the proposal are to put together a team to find a cure"
                "for Poverty, and then to find it"
            ],
            "importance": ["save lives", "lift people from poverty"],
            "institutions": [],
            "month": "May",
            "names": ["A Genius"],
            "nsf_broader_impacts": ["Poor people will be made unpoor"],
            "nsf_create_original_transformative": [
                "transformative because lives will be transformed"
            ],
            "nsf_plan_good": [
                "I don't see any issues with the plan",
                "it should be very straightforward",
            ],
            "nsf_pot_to_advance_knowledge": ["This won't advance knowledge at all"],
            "nsf_pot_to_benefit_society": [
                "Society will benefit by poor people being made unpoor if they want "
                "to be"
            ],
            "requester": "Tessemer Guebre",
            "reviewer": "sbillinge",
            "status": "submitted",
            "summary": "dynamite proposal",
            "title": "A stunning new way to cure Poverty",
            "year": 2019,
        },
    ],
    "proposals": [
        {
            "_id": "mypropsal",
            "amount": 1000000.0,
            "authors": ["Anthony Scopatz", "Robert Flanagan"],
            "begin_day": 1,
            "begin_month": "May",
            "begin_year": 2030,
            "currency": "USD",
            "submitted_day": 18,
            "duration": 3,
            "end_day": 31,
            "end_month": "December",
            "end_year": 2030,
            "full": {
                "benefit_of_collaboration": "http://pdf.com"
                "/benefit_of_collaboration",
                "cv": ["http://pdf.com/scopatz-cv", "http://pdf.com/flanagan-cv"],
                "narrative": "http://some.com/pdf",
            },
            "submitted_month": "Aug",
            "notes": "Quite an idea",
            "pi": "Anthony Scopatz",
            "pre": {
                "benefit_of_collaboration": "http://pdf.com"
                "/benefit_of_collaboration",
                "cv": ["http://pdf.com/scopatz-cv", "http://pdf.com/flanagan-cv"],
                "day": 2,
                "month": "Aug",
                "narrative": "http://some.com/pdf",
                "year": 1998,
            },
            "status": "submitted",
            "title": "A very fine proposal indeed",
            "submitted_year": 1999,
        },
        {
            "_id": "dmref15",
            "amount": 982785.0,
            "authors": ["qdu", "dhsu", "sbillinge"],
            "call_for_proposals": "http://www.nsf.gov/pubs/2014/nsf14591/"
            "nsf14591.htm",
            "begin_day": 1,
            "begin_month": "May",
            "begin_year": 2018,
            "cpp_info": {
                "cppflag": True,
                "other_agencies_submitted": "None",
                "institution": "Columbia University",
                "person_months_academic": 0,
                "person_months_summer": 1,
                "project_scope": "lots to do but it doesn't overlap with any "
                "other of my grants",
                "single_pi": True,
            },
            "currency": "USD",
            "submitted_date": "2015-02-02",
            "duration": 3,
            "end_day": 1,
            "end_month": "May",
            "end_year": 2019,
            "funder": "NSF",
            "notes": "Quite an idea",
            "pi": "Simon Billinge",
            "status": "accepted",
            "team": [
                {
                    "institution": "Columbia University",
                    "name": "qdu",
                    "position": "copi",
                },
                {
                    "institution": "Columbia University",
                    "name": "dhsu",
                    "position": "copi",
                },
                {
                    "institution": "Columbia University",
                    "name": "sbillinge",
                    "position": "pi",
                    "subaward_amount": 330000.0,
                },
            ],
            "title": "DMREF: Novel, data validated, nanostructure determination "
            "methods for accelerating materials discovery",
            "title_short": "DMREF nanostructure",
        },
        {
            "_id": "SymPy-1.1",
            "amount": 3000.0,
            "begin_date": "2030-05-01",
            "end_date": "2030-12-31",
            "cpp_info": {
                "cppflag": True,
                "other_agencies_submitted": "None",
                "institution": "Columbia University",
                "person_months_academic": 0,
                "person_months_summer": 1,
                "project_scope": "",
            },
            "currency": "USD",
            "pi": "Anthony Scopatz",
            "status": "pending",
            "team": [
                {
                    "institution": "Columbia University",
                    "name": "scopatz",
                    "position": "pi",
                }
            ],
            "title": "SymPy 1.1 Release Support",
        },
        {
            "_id": "SymPy-2.0",
            "amount": 3000.0,
            "begin_date": "2019-06-01",
            "end_date": "2030-12-31",
            "cpp_info": {
                "cppflag": True,
                "other_agencies_submitted": "None",
                "institution": "Columbia University",
                "person_months_academic": 0,
                "person_months_summer": 1,
                "project_scope": "",
            },
            "currency": "USD",
            "pi": "sbillinge",
            "status": "accepted",
            "title": "SymPy 1.1 Release Support",
        },
        {
            "_id": "abc42",
            "amount": 42000.0,
            "begin_date": "2020-06-01",
            "end_date": "2020-12-31",
            "cpp_info": {
                "cppflag": True,
                "other_agencies_submitted": "None",
                "institution": "Columbia University",
                "person_months_academic": 0,
                "person_months_summer": 1,
                "project_scope": "",
            },
            "currency": "USD",
            "pi": "sbillinge",
            "status": "submitted",
            "title": "The answer to life, the universe, and everything",
        },
    ],
    "reading_lists": [
        {
            "_id": "getting_started_with_pdf",
            "day": 15,
            "month": 12,
            "papers": [
                {
                    "doi": "10.1107/97809553602060000935",
                    "text": "Very basic, but brief, intro to powder diffraction in general",
                },
                {
                    "doi": "10.1039/9781847558237-00464",
                    "text": "Lightest weight overview of PDF analysis around.  Good starting point",
                },
                {
                    "url": "http://www.diffpy.org",
                    "text": "Download and install PDFgui software and run through the step by step tutorial under the help tab",
                },
            ],
            "purpose": "Beginning reading about PDF",
            "title": "A step-by-step pathway towards PDF understanding.  It is recommended to read the papers in the order they are listed here.",
            "year": 2019,
        },
        {
            "_id": "african_swallows",
            "date": "2019-12-01",
            "papers": [
                {
                    "doi": "10.1107/97809553602060000935",
                    "text": "Very basic, but brief, intro to african swallows",
                },
            ],
            "title": "A step-by-step pathway towards african swallow understanding.",
        },
    ],
    "refereeReports": [
        {
            "_id": "1902nature",
            "claimed_found_what": ["gravity waves"],
            "claimed_why_important": ["more money for ice cream"],
            "did_how": ["measured with a ruler"],
            "did_what": ["found a much cheaper way to measure gravity waves"],
            "due_date": "2020-04-11",
            "editor_eyes_only": "to be honest, I don't believe a word of it",
            "final_assessment": ["The authors should really start over"],
            "first_author_last_name": "Wingit",
            "freewrite": "this comment didn't fit anywhere above",
            "journal": "Nature",
            "month": "jun",
            "recommendation": "reject",
            "requester": "Max Planck",
            "reviewer": "sbillinge",
            "status": "submitted",
            "submitted_date": "2019-01-01",
            "title": "a ruler approach to measuring gravity waves",
            "validity_assessment": ["complete rubbish"],
            "year": 2019,
        },
        {
            "_id": "2002nature",
            "claimed_found_what": ["more gravity waves"],
            "claimed_why_important": ["even more money for ice cream"],
            "did_how": ["measured with a ruler"],
            "did_what": ["found an even cheaper way to measure gravity waves"],
            "due_date": "2021-04-11",
            "editor_eyes_only": "to be honest, I don't believe a word of it",
            "final_assessment": ["The authors should really start over"],
            "first_author_last_name": "Wingit",
            "freewrite": "this comment didn't fit anywhere above",
            "journal": "Nature",
            "month": "jun",
            "recommendation": "reject",
            "requester": "Max Planck",
            "reviewer": "sbillinge",
            "status": "accepted",
            "submitted_date": "2020-01-01",
            "title": "an even smaller ruler approach to measuring gravity waves",
            "validity_assessment": ["complete rubbish"],
            "year": 2020,
        },
    ],
    "students": {
        "_id": "Human A. Person",
        "aka": ["H. A. Person"],
        "email": "haperson@uni.edu",
        "university_id": "HAP42",
    },
    "todos": [
        {"_id": "ascopatz"},
        {
            "_id": "sbillinge",
            "todos": [
                {
                    "description": "read paper",
                    "uuid": "1saefadf-wdaagea2",
                    "due_date": "2020-07-19",
                    "begin_date": "2020-06-15",
                    "deadline": True,
                    "duration": 60.0,
                    "importance": 2,
                    "status": "started",
                    "assigned_by": "scopatz",
                    "running_index": 1,
                    "tags": ["reading", "downtime"],
                },
                {
                    "description": "prepare the presentation",
                    "uuid": "2saefadf-wdaagea3",
                    "due_date": "2020-07-29",
                    "begin_date": "2020-06-22",
                    "duration": 30.0,
                    "importance": 0,
                    "status": "started",
                    "notes": [
                        "about 10 minutes",
                        "don't forget to upload to the website",
                    ],
                    "assigned_by": "sbillinge",
                    "running_index": 2,
                    "tags": ["downtime"],
                },
            ],
        },
    ],
}

SCHEMAS = load_schemas()

for s in SCHEMAS:
    SCHEMAS[s]["files"] = {
        "description": "Files associated with the document",
        # TODO: fix this since this is currently comming out a CommentedMap (+1: Yevgeny)
        # "type": "list",
        # "schema": {"type": "string"},
        "required": False,
    }


class NoDescriptionValidator(Validator):
    def _validate_description(self, description, field, value):
        """Don't validate descriptions

        The rule's arguments are validated against this schema:
        {'type': 'string'}"""
        if False:
            pass

    def _validate_eallowed(self, eallowed, field, value):
        """Test if value is in list
        The rule's arguments are validated against this schema:
        {'type': 'list'}
        """
        if value not in eallowed:
            warn(
                '"{}" is not in the preferred entries for "{}", please '
                "consider changing this entry to conform or add this to the "
                "``eallowed`` field in the schema.".format(value, field)
            )


def validate(coll, record, schemas):
    """Validate a record for a given db

    Parameters
    ----------
    coll : str
        The name of the db in question
    record : dict
        The record to be validated
    schemas : dict
        The schema to validate against

    Returns
    -------
    rtn : bool
        True is valid
    errors: dict
        The errors encountered (if any)

    """
    if coll in schemas:
        schema = copy.deepcopy(schemas[coll])
        v = NoDescriptionValidator(schema)
        return v.validate(record), v.errors
    else:
        return True, ()
