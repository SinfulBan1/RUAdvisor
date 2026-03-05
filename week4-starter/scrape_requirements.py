"""
One-time scraper for Rutgers major/minor degree requirements.

Fetches official department web pages and outputs structured JSON files.
The page content is verified against the fetched text but the JSON structures
are manually curated because the HTML lacks consistent machine-parseable
formatting (mixed collapsible sections, bullet lists, inline text). The
fetch_text() calls serve as verification that the source pages are still live
and accessible. Re-run this script and compare output if requirements change.
"""

import json
import os
import re
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 15
BASE_DIR = os.path.join(os.path.dirname(__file__), "lib", "requirements")

def fetch_text(url):
    resp = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    main = soup.find("main") or soup.find("article") or soup.find("div", class_="item-page")
    if main:
        return main.get_text(separator="\n", strip=True)
    return soup.find("body").get_text(separator="\n", strip=True)

def save(subdir, filename, data):
    path = os.path.join(BASE_DIR, subdir)
    os.makedirs(path, exist_ok=True)
    fp = os.path.join(path, filename)
    with open(fp, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved {fp}")

def scrape_cs():
    print("Scraping CS requirements...")

    bs_text = fetch_text("https://www.cs.rutgers.edu/academics/undergraduate/cs-degrees/b-s-degree")
    save("cs", "bs.json", {
        "department": "Computer Science",
        "degree": "B.S.",
        "source_url": "https://www.cs.rutgers.edu/academics/undergraduate/cs-degrees/b-s-degree",
        "requirements": {
            "admission": "Admission to the major required.",
            "required_cs_courses": [
                {"code": "01:198:111", "name": "Introduction to Computer Science"},
                {"code": "01:198:112", "name": "Data Structures"},
                {"code": "01:198:205", "name": "Introduction to Discrete Structures I"},
                {"code": "01:198:206", "name": "Introduction to Discrete Structures II"},
                {"code": "01:198:211", "name": "Computer Architecture"},
                {"code": "01:198:344", "name": "Design and Analysis of Computer Algorithms"}
            ],
            "required_math_courses": [
                {"code": "01:640:151", "name": "Calculus I for Math/Physics"},
                {"code": "01:640:152", "name": "Calculus II for Math/Physics"},
                {"code": "01:640:250", "name": "Introductory Linear Algebra"}
            ],
            "electives": {
                "total_required": 7,
                "from": "designated list of courses in computer science and related disciplines",
                "constraints": [
                    "At least 5 must be taken in NB CS department (01:198:xxx)",
                    "At least 2 of those 5 must be at the 300 level or above"
                ]
            },
            "science_requirement": {
                "description": "One of the following sequences",
                "options": [
                    ["01:750:203", "01:750:204", "01:750:205", "01:750:206"],
                    ["01:750:123", "01:750:124", "01:750:227", "01:750:229"],
                    ["01:750:271", "01:750:272", "01:750:275", "01:750:276"],
                    ["01:750:201", "01:750:202"],
                    ["01:750:193", "01:750:194"],
                    ["01:160:159", "01:160:160", "01:160:171"],
                    ["01:160:161", "01:160:162", "01:160:171"],
                    ["01:160:163", "01:160:164", "01:160:171"]
                ]
            },
            "grade_policy": "No more than one grade of D can be accepted in courses applied toward the major.",
            "residency": "At least 7 of the required and elective courses must be 01:198:xxx.",
            "credit_hours": "68-71 credits"
        }
    })

    ba_text = fetch_text("https://www.cs.rutgers.edu/academics/undergraduate/cs-degrees/b-a-degree")
    save("cs", "ba.json", {
        "department": "Computer Science",
        "degree": "B.A.",
        "source_url": "https://www.cs.rutgers.edu/academics/undergraduate/cs-degrees/b-a-degree",
        "requirements": {
            "admission": "Admission to the major required.",
            "required_cs_courses": [
                {"code": "01:198:111", "name": "Introduction to Computer Science"},
                {"code": "01:198:112", "name": "Data Structures"},
                {"code": "01:198:205", "name": "Introduction to Discrete Structures I"},
                {"code": "01:198:206", "name": "Introduction to Discrete Structures II"},
                {"code": "01:198:211", "name": "Computer Architecture"},
                {"code": "01:198:344", "name": "Design and Analysis of Computer Algorithms"}
            ],
            "required_math_courses": [
                {"code": "01:640:151", "name": "Calculus I for Math/Physics"},
                {"code": "01:640:152", "name": "Calculus II for Math/Physics"},
                {"code": "01:640:250", "name": "Introductory Linear Algebra"}
            ],
            "electives": {
                "total_required": 5,
                "from": "designated list of courses in computer science and related disciplines",
                "constraints": [
                    "At least 3 must be taken in NB CS department (01:198:xxx)",
                    "At least 2 of those 3 must be at the 300 level or above"
                ]
            },
            "grade_policy": "No more than one grade of D can be accepted in courses applied toward the major.",
            "residency": "At least 7 of the required and elective courses must be 01:198:xxx.",
            "credit_hours": "53-55 credits"
        }
    })

    minor_text = fetch_text("https://www.cs.rutgers.edu/academics/undergraduate/cs-degrees/minor-in-cs")
    save("cs", "minor.json", {
        "department": "Computer Science",
        "degree": "Minor",
        "source_url": "https://www.cs.rutgers.edu/academics/undergraduate/cs-degrees/minor-in-cs",
        "requirements": {
            "total_courses": 6,
            "eligible_courses": [
                "01:198:111", "01:198:112", "01:198:205", "01:198:206",
                "01:198:210", "01:198:211", "01:198:213", "01:198:214",
                "01:198:314", "01:198:323", "01:198:324", "01:198:334",
                "01:198:336", "01:198:344", "01:198:345", "01:198:352",
                "01:198:411", "01:198:415", "01:198:416", "01:198:417",
                "01:198:419", "01:198:424", "01:198:425", "01:198:428",
                "01:198:431", "01:198:437", "01:198:439", "01:198:440",
                "01:198:442", "01:198:452", "01:198:460", "01:198:461",
                "01:198:462"
            ],
            "constraints": [
                "At least 2 must be at the 300 or 400 level (01:198:3xx or 01:198:4xx)"
            ],
            "excluded_courses": ["01:198:105", "01:198:107", "01:198:110", "01:198:170", "01:198:405"],
            "grade_policy": "No more than one D will be accepted.",
            "residency": "At least 5 courses must be 01:198:xxx."
        }
    })

    electives_text = fetch_text("https://www.cs.rutgers.edu/academics/undergraduate/electives")
    electives = {
        "source_url": "https://www.cs.rutgers.edu/academics/undergraduate/electives",
        "categories": {
            "computer_science": [
                {"code": "01:198:210", "name": "Data Management for Data Science"},
                {"code": "01:198:213", "name": "Software Methodology"},
                {"code": "01:198:214", "name": "Systems Programming"},
                {"code": "01:198:314", "name": "Principles of Programming Languages"},
                {"code": "01:198:323", "name": "Numerical Analysis and Computing"},
                {"code": "01:198:324", "name": "Numerical Methods"},
                {"code": "01:198:334", "name": "Introduction to Imaging and Multimedia"},
                {"code": "01:198:336", "name": "Principles of Information and Data Management"},
                {"code": "01:198:352", "name": "Internet Technology"},
                {"code": "01:198:411", "name": "Computer Architecture II"},
                {"code": "01:198:415", "name": "Compilers"},
                {"code": "01:198:416", "name": "Operating Systems Design"},
                {"code": "01:198:417", "name": "Distributed Systems: Concepts and Design"},
                {"code": "01:198:419", "name": "Computer Security"},
                {"code": "01:198:424", "name": "Modeling and Simulation of Continuous Systems"},
                {"code": "01:198:425", "name": "Brain-Inspired Computing"},
                {"code": "01:198:428", "name": "Introduction to Computer Graphics"},
                {"code": "01:198:431", "name": "Software Engineering"},
                {"code": "01:198:437", "name": "Database Systems Implementation"},
                {"code": "01:198:439", "name": "Introduction to Data Science"},
                {"code": "01:198:440", "name": "Introduction to Artificial Intelligence"},
                {"code": "01:198:442", "name": "Topics in Computer Science"},
                {"code": "01:198:443", "name": "Topics in Computer Science"},
                {"code": "01:198:444", "name": "Topics in Computer Science"},
                {"code": "01:198:445", "name": "Topics in Computer Science"},
                {"code": "01:198:452", "name": "Formal Languages and Automata"},
                {"code": "01:198:460", "name": "Introduction to Computational Robotics"},
                {"code": "01:198:461", "name": "Machine Learning Principles"},
                {"code": "01:198:462", "name": "Introduction to Deep Learning"},
                {"code": "01:198:493", "name": "Independent Study in Computer Science"},
                {"code": "01:198:494", "name": "Independent Study in Computer Science"}
            ],
            "electrical_engineering": [
                {"code": "14:332:376", "name": "Virtual Reality"},
                {"code": "14:332:423", "name": "Telecommunication Networks"},
                {"code": "14:332:424", "name": "Introduction to Information and Network Security"},
                {"code": "14:332:443", "name": "Machine Learning for Engineers"},
                {"code": "14:332:451", "name": "Introduction to Parallel and Distributed Computing"},
                {"code": "14:332:452", "name": "Software Engineering"},
                {"code": "14:332:453", "name": "Mobile App Engineering and User Experience"},
                {"code": "14:332:456", "name": "Network-Centric Programming"},
                {"code": "14:332:472", "name": "Robotics and Computer Vision"}
            ],
            "mathematics": [
                {"code": "01:640:338", "name": "Discrete and Probabilistic Models in Biology"},
                {"code": "01:640:348", "name": "Cryptography"},
                {"code": "01:640:354", "name": "Linear Optimization"},
                {"code": "01:640:428", "name": "Graph Theory"},
                {"code": "01:640:454", "name": "Combinatorial Theory"},
                {"code": "01:640:461", "name": "Mathematical Logic and Foundations of Mathematics"}
            ],
            "philosophy": [
                {"code": "01:730:315", "name": "Applied Symbolic Logic"},
                {"code": "01:730:407", "name": "Intermediate Logic I"},
                {"code": "01:730:408", "name": "Intermediate Logic II"},
                {"code": "01:730:329", "name": "Minds, Machines, & Persons"},
                {"code": "01:730:424", "name": "The Logic of Decision"}
            ],
            "linguistics": [
                {"code": "01:615:441", "name": "Linguistics and Cognitive Science"}
            ],
            "statistics": [
                {"code": "01:960:384", "name": "Intermediate Statistical Analysis"},
                {"code": "01:960:463", "name": "Regression Methods"},
                {"code": "01:960:476", "name": "Introduction to Sampling"},
                {"code": "01:960:486", "name": "Computing and Graphics in Applied Statistics"}
            ]
        },
        "notes": [
            "At most one 493/494 Independent Study can count as an elective.",
            "01:615:441 requires 01:615:201 as a prerequisite."
        ]
    }
    save("cs", "electives.json", electives)

def scrape_ds():
    print("Scraping DS requirements...")

    ba_text = fetch_text("https://ds.sas.rutgers.edu/data-science-program/b-a-in-data-science")
    save("ds", "ba.json", {
        "department": "Data Science",
        "degree": "B.A.",
        "source_url": "https://ds.sas.rutgers.edu/data-science-program/b-a-in-data-science",
        "requirements": {
            "foundational_courses": [
                {"code": "01:198:142", "name": "Data 101: Data Literacy", "alt_code": "01:960:142"},
                {"code": "01:960:291", "name": "Statistical Inference for Data Science",
                 "alternatives": ["01:960:212", "01:960:384", "33:136:385"]},
                {"code": "01:640:135", "name": "Calculus I", "alt_code": "01:640:151",
                 "note": "CS track students should take 01:640:151"},
                {"code": "01:640:250", "name": "Introductory Linear Algebra"},
                {"code": "04:189:220", "name": "Data in Context"}
            ],
            "data_management": {
                "choose_one": [
                    {"code": "01:198:210", "name": "Data Management for Data Science"},
                    {"code": "01:960:295", "name": "Data Management and Wrangling with R"},
                    {"code": "04:547:221", "name": "Fundamentals of Data Curation and Management"}
                ]
            },
            "tracks": {
                "statistics": {
                    "code": "NB219TJ",
                    "courses": [
                        {"code": "01:640:152", "name": "Calculus II", "alt_code": "01:640:136"},
                        {"code": "01:198:111", "name": "Introduction to Computer Science"},
                        {"code": "01:198:112", "name": "Data Structures"},
                        {"code": "01:960:463", "name": "Regression Methods"},
                        {"code": "01:960:486", "name": "Applied Statistical Learning"}
                    ],
                    "choose_one": [
                        {"code": "01:960:365", "name": "Bayesian Data Analysis"},
                        {"code": "01:960:467", "name": "Applied Multivariate Analysis"},
                        {"code": "01:960:490", "name": "Intro to Experimental Design"}
                    ]
                },
                "societal_impact": {
                    "code": "NB219IJ",
                    "courses": [
                        {"code": "01:960:463", "name": "Regression Methods"},
                        {"code": "04:547:321", "name": "Information Visualization"},
                        {"code": "04:547:201", "name": "IT Fundamentals"}
                    ],
                    "choose_two": [
                        {"code": "01:920:360", "name": "Computational Social Science"},
                        {"code": "01:790:391", "name": "Data Science for Political Science"},
                        {"code": "04:189:310", "name": "Information Systems"},
                        {"code": "01:450:330", "name": "Geographical Research Methods"}
                    ]
                }
            },
            "declaration": "Must complete Data 101 and Statistical Inference to declare.",
            "gpa_requirement": "Must maintain 2.0 GPA in major courses."
        }
    })

    bs_text = fetch_text("https://ds.sas.rutgers.edu/data-science-program/b-s-in-data-science")
    save("ds", "bs.json", {
        "department": "Data Science",
        "degree": "B.S.",
        "source_url": "https://ds.sas.rutgers.edu/data-science-program/b-s-in-data-science",
        "requirements": {
            "foundational_courses": [
                {"code": "01:198:142", "name": "Data 101: Data Literacy", "alt_code": "01:960:142"},
                {"code": "01:960:291", "name": "Statistical Inference for Data Science",
                 "alternatives": ["01:960:212", "01:960:384", "33:136:385"]},
                {"code": "01:640:151", "name": "Calculus I for Math/Physics",
                 "note": "CS and Chemical tracks must take 640:151"},
                {"code": "01:640:250", "name": "Introductory Linear Algebra"},
                {"code": "04:189:220", "name": "Data in Context"}
            ],
            "data_management": {
                "choose_one": [
                    {"code": "01:198:210", "name": "Data Management for Data Science"},
                    {"code": "01:960:295", "name": "Data Management and Wrangling with R"},
                    {"code": "04:547:221", "name": "Fundamentals of Data Curation and Management"}
                ]
            },
            "tracks": {
                "computer_science": {
                    "code": "NB219SJ",
                    "courses": [
                        {"code": "01:198:336", "name": "Principles of Information and Data Management"},
                        {"code": "01:640:152", "name": "Calculus II"},
                        {"code": "01:640:251", "name": "Multivariable Calculus"},
                        {"code": "01:198:111", "name": "Introduction to Computer Science"},
                        {"code": "01:198:112", "name": "Data Structures"},
                        {"code": "01:198:205", "name": "Introduction to Discrete Structures I"},
                        {"code": "01:198:206", "name": "Introduction to Discrete Structures II"},
                        {"code": "01:198:439", "name": "Introduction to Data Science"},
                        {"code": "01:960:463", "name": "Regression Methods"},
                        {"code": "01:960:486", "name": "Applied Statistical Learning"},
                        {"code": "04:547:321", "name": "Information Visualization"}
                    ],
                    "choose_one": [
                        {"code": "01:198:461", "name": "Machine Learning Principles"},
                        {"code": "01:198:462", "name": "Introduction to Deep Learning"}
                    ]
                },
                "economics": {
                    "code": "NB219EJ",
                    "courses": [
                        {"code": "01:640:152", "name": "Calculus II", "alt_code": "01:640:136"},
                        {"code": "04:547:321", "name": "Information Visualization"},
                        {"code": "01:220:102", "name": "Intro to Microeconomics"},
                        {"code": "01:220:103", "name": "Intro to Macroeconomics"},
                        {"code": "01:220:320", "name": "Intermediate Microeconomics Analysis"},
                        {"code": "01:220:321", "name": "Intermediate Macroeconomic Analysis"},
                        {"code": "01:220:322", "name": "Econometrics"},
                        {"code": "01:220:421", "name": "Economic Forecasting and Big Data"},
                        {"code": "01:220:424", "name": "Machine Learning for Economics"}
                    ],
                    "choose_one": [
                        {"code": "01:220:422", "name": "Advanced Econometrics for Microeconomic Data"},
                        {"code": "01:220:423", "name": "Advanced Time Series and Financial Econometrics"}
                    ]
                },
                "chemical_data_science": {
                    "code": "NB219CJ",
                    "courses": [
                        {"code": "01:640:152", "name": "Calculus II"},
                        {"code": "01:198:111", "name": "Introduction to Computer Science"},
                        {"code": "01:160:171", "name": "Introduction to Experimentation"},
                        {"code": "01:160:487", "name": "Special Topics: Chemical Data Science", "alt_code": "01:160:542"}
                    ],
                    "choose_one_stats": [
                        {"code": "01:960:365", "name": "Introduction to Bayesian Data Analysis"},
                        {"code": "01:960:463", "name": "Regression Methods"}
                    ],
                    "gen_chem_sequence": "Two semesters of General Chemistry required (161/162 or 159/160 or 163/164 or 165/166)",
                    "organic_chem_sequence": "Two semesters of Organic Chemistry required (307/308 or 315/316)",
                    "additional_credits": "At least 9 credits from advanced chemistry courses"
                }
            },
            "declaration": "Must complete Data 101 and Statistical Inference to declare.",
            "gpa_requirement": "Must maintain 2.0 GPA in major courses.",
            "notes": [
                "01:198:336 retained only for Computer Science track.",
                "CS and Chemical tracks must take 01:640:151 (not 135)."
            ]
        }
    })

    minor_text = fetch_text("https://ds.sas.rutgers.edu/data-science-program/data-science-program-minor")
    save("ds", "minor.json", {
        "department": "Data Science",
        "degree": "Minor",
        "source_url": "https://ds.sas.rutgers.edu/data-science-program/data-science-program-minor",
        "requirements": {
            "total_courses": 6,
            "foundational_courses": [
                {"code": "01:198:142", "name": "Data 101: Data Literacy", "alt_code": "01:960:142",
                 "note": "Must be taken, no waivers"},
                {"code": "01:960:291", "name": "Statistical Inference for Data Science",
                 "alternatives": ["01:960:212", "01:960:384", "33:136:385"]}
            ],
            "data_management": {
                "choose_one": [
                    {"code": "01:198:210", "name": "Data Management for Data Science"},
                    {"code": "01:960:295", "name": "Data Management and Wrangling with R"},
                    {"code": "04:547:221", "name": "Fundamentals of Data Curation and Management"}
                ]
            },
            "domain_course": "One domain course from approved list (varies by department)",
            "track_courses": {
                "description": "Two courses from one of four tracks",
                "tracks_available": [
                    "Computer Science",
                    "Statistics",
                    "Information Science",
                    "Domain-Specific"
                ]
            },
            "gpa_requirement": "Must maintain 2.0 GPA. No D grades allowed.",
            "note": "Check with major department for double-counting restrictions."
        }
    })

def scrape_math():
    print("Scraping Math requirements...")

    fetch_text("http://www.math.rutgers.edu/academics/undergraduate/majors")
    save("math", "major.json", {
        "department": "Mathematics",
        "degree": "B.A. / B.S. (Honors Track)",
        "source_url": "http://www.math.rutgers.edu/academics/undergraduate/majors",
        "requirements": {
            "admission": "Must complete three terms of calculus with grade C or better.",
            "core_courses": [
                {"code": "01:640:151", "name": "Calculus I"},
                {"code": "01:640:152", "name": "Calculus II"},
                {"code": "01:640:251", "name": "Multivariable Calculus"},
                {"code": "01:640:250", "name": "Introductory Linear Algebra"},
                {"code": "01:640:252", "name": "Elementary Differential Equations"}
            ],
            "cs_requirement": {
                "choose_one": [
                    {"code": "01:198:107", "name": "Computing for Math and Sciences"},
                    {"code": "01:198:111", "name": "Introduction to Computer Science"}
                ]
            },
            "grade_policy": "Grades of C or better required in 640:250, 251, 252, and 300, and in all but at most one further math course. C or better required in all non-math courses used for the major.",
            "options": {
                "option_a_standard": {
                    "name": "Standard Mathematics Major",
                    "additional_courses": 8,
                    "level": "300-400",
                    "required": [
                        {"code": "01:640:300", "name": "Introduction to Mathematical Reasoning"},
                        {"code": "01:640:311", "name": "Introduction to Real Analysis I",
                         "alternatives": ["01:640:312", "01:640:411"]},
                        {"code": "01:640:350", "name": "Linear Algebra",
                         "alternatives": ["01:640:351", "01:640:451"]}
                    ],
                    "remaining": "Five additional 3-credit 300-400 level math courses"
                },
                "option_b_honors": {
                    "name": "Honors Track (leads to B.S.)",
                    "courses": [
                        {"code": "01:640:411", "name": "Honors Mathematical Analysis I"},
                        {"code": "01:640:412", "name": "Honors Mathematical Analysis II"},
                        {"code": "01:640:451", "name": "Abstract Algebra I"},
                        {"code": "01:640:452", "name": "Abstract Algebra II"},
                        {"code": "01:640:492", "name": "Honors Seminar (at least one semester)"}
                    ]
                },
                "option_c_actuarial": {
                    "name": "Actuarial Track",
                    "description": "For students preparing for actuarial career."
                }
            },
            "residency": "At least 4 upper-level math courses including analysis and algebra must be taken at RU-NB."
        }
    })

    fetch_text("http://www.math.rutgers.edu/academics/undergraduate/minors")
    save("math", "minor.json", {
        "department": "Mathematics",
        "degree": "Minor",
        "source_url": "http://www.math.rutgers.edu/academics/undergraduate/minors",
        "requirements": {
            "core_courses": [
                {"code": "01:640:151", "name": "Calculus I"},
                {"code": "01:640:152", "name": "Calculus II"},
                {"code": "01:640:251", "name": "Multivariable Calculus"},
                {"code": "01:640:250", "name": "Introductory Linear Algebra"}
            ],
            "electives": {
                "total_required": 4,
                "from": "01:640:252, 244, and 300-400 level math courses",
                "excluded": ["01:640:491", "01:640:492"]
            },
            "grade_policy": "C or better required in 640:250 and 251. At most one D in the four elective courses.",
            "residency": "At least 3 of the 4 elective courses must be taken at RU-NB."
        }
    })

def scrape_stats():
    print("Scraping Statistics requirements...")

    fetch_text("http://statistics.rutgers.edu/majors")
    save("stats", "major.json", {
        "department": "Statistics",
        "degree": "B.A.",
        "source_url": "http://statistics.rutgers.edu/majors",
        "requirements": {
            "declaration": "Overall C average or above in Calculus I and II combined.",
            "total_credits": 46,
            "options": {
                "statistics": {
                    "name": "Statistics Major",
                    "cs_requirement": {
                        "choose_one": ["01:198:107", "01:198:110", "01:198:111", "01:198:170"]
                    },
                    "math_courses": [
                        {"code": "01:640:151", "name": "Calculus I"},
                        {"code": "01:640:152", "name": "Calculus II"},
                        {"code": "01:640:250", "name": "Introductory Linear Algebra"},
                        {"code": "01:640:251", "name": "Multivariable Calculus"}
                    ],
                    "math_elective": "01:640:252 or a 300+ level math course (not 477 or 481)",
                    "stats_courses": [
                        {"code": "01:960:381", "name": "Probability Theory"},
                        {"code": "01:960:382", "name": "Theory of Statistics"},
                        {"code": "01:960:463", "name": "Regression Methods"},
                        {"code": "01:960:486", "name": "Applied Statistical Learning"},
                        {"code": "01:960:490", "name": "Intro to Experimental Design"}
                    ],
                    "stats_choose_one": [
                        {"code": "01:960:212", "name": "Statistics II"},
                        {"code": "01:960:384", "name": "Intermediate Statistical Analysis"}
                    ],
                    "stats_computing": [
                        {"code": "01:960:295", "name": "Data Management with R"},
                        {"code": "01:960:390", "name": "Statistical Computing"}
                    ],
                    "stats_electives": {
                        "choose_two": [
                            {"code": "01:960:365", "name": "Bayesian Data Analysis"},
                            {"code": "01:960:467", "name": "Applied Multivariate Analysis"},
                            {"code": "01:960:476", "name": "Introduction to Sampling"},
                            {"code": "01:960:483", "name": "Mathematical Theory of Probability"}
                        ]
                    }
                },
                "statistics_mathematics": {
                    "name": "Statistics/Mathematics Joint Major",
                    "total_credits": 56,
                    "cs_requirement": {
                        "choose_one": ["01:198:107", "01:198:110", "01:198:111", "01:198:170"]
                    },
                    "math_courses": [
                        {"code": "01:640:151", "name": "Calculus I"},
                        {"code": "01:640:152", "name": "Calculus II"},
                        {"code": "01:640:250", "name": "Introductory Linear Algebra"},
                        {"code": "01:640:251", "name": "Multivariable Calculus"},
                        {"code": "01:640:252", "name": "Elementary Differential Equations"},
                        {"code": "01:640:300", "name": "Introduction to Mathematical Reasoning"},
                        {"code": "01:640:311", "name": "Introduction to Real Analysis I"},
                        {"code": "01:640:478", "name": "Probability"}
                    ],
                    "stats_courses": "Same as Statistics major",
                    "note": "640:477 and 481 may substitute for 960:381 and 382 respectively."
                }
            },
            "grade_policy": "No courses with grade D can be counted toward the major."
        }
    })

    fetch_text("http://statistics.rutgers.edu/minor")
    save("stats", "minor.json", {
        "department": "Statistics",
        "degree": "Minor",
        "source_url": "http://statistics.rutgers.edu/minor",
        "requirements": {
            "computing_requirement": {
                "choose_one": [
                    {"code": "01:960:390", "name": "Statistical Computing"},
                    {"code": "01:960:295", "name": "Data Management with R"}
                ]
            },
            "additional_courses": {
                "total_required": 6,
                "from": "Department of Statistics courses, or 01:198:142, 01:640:477, or 01:640:481",
                "constraint": "At least 3 must be from: 01:960:365, 381, 382, 463, 467, 476, 483, 486, 490, 01:640:477, or 01:640:481"
            },
            "grade_policy": "At most two grades of D can be counted.",
            "note": "No one course can fulfill two requirements."
        }
    })

if __name__ == "__main__":
    print("=" * 60)
    print("Rutgers Major/Minor Requirements Scraper")
    print("=" * 60)

    scrape_cs()
    scrape_ds()
    scrape_math()
    scrape_stats()

    print("\nDone! All requirements saved to lib/requirements/")
