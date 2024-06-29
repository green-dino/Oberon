CONTROL_GROUPS = {
    "SEC-ARCH": {"Description": "Security Architect", "Email":
"secarch@example.com"},
    "SYS-ARCH": {"Description": "Systems Architect", "Email":
"sysarch@example.com"},
    "SOFT-DEV": {"Description": "Software Developer", "Email":
"softdev@example.com"},
    "DATA-ARCH": {"Description": "Data Architect", "Email":
"dataarch@example.com"},
    "ENT-ARCH": {"Description": "Enterprise Architect", "Email":
"entarch@example.com"},
    "TECH-ARCH": {"Description": "Technology Architect", "Email":
"techarch@example.com"},
    "CYBER-ANALYST": {"Description": "Cyber Defense Analyst", "Email":
"cyberanalyst@example.com"},
    "CYBER-INFRA": {"Description": "Cyber Defense Infrastructure Support",
"Email": "cyberinfra@example.com"},
    "DATA-ANALYST": {"Description": "Data Analyst", "Email":
"dataanalyst@example.com"},
    "SYS-DEV": {"Description": "Systems Developer", "Email":
"sysdev@example.com"},
    "NET-ENG": {"Description": "Network Engineer", "Email":
"neteng@example.com"},
    "SYS-ADMIN": {"Description": "Systems Administrator", "Email":
"sysadmin@example.com"},
    "SEC-ASSESSOR": {"Description": "Secure Software Assessor", "Email":
"secassessor@example.com"},
    "SEC-CONT-ASSESSOR": {"Description": "Security Control Assessor",
"Email": "seccontassessor@example.com"}
}


data = {
    "Phases": {
        "A": "Identify",
        "B": "Protect",
        "C": "Detect",
        "D": "Respond",
        "E": "Recover"
    },
    "Control Group": {
        "F": "Control Short Number",
        "G": "Description of the Control",
        "H": "Discussion Questions",
        "I": "Files / Evidence",
        "J": "Status",
        "K": "Priority",
        "L": "Selected",
        "M": "Last Updated",
        "N": "Requirements",
        "O": "Estimate",
        "P": "Design",
        "Q": "Implementation",
        "R": "Project Timeline",
        "S": "Start",
        "T": "End",
        "U": "Responsible Team",
        "V": "Team Members",
        "W": "Maintenance",
        "X": "Review Date",
        "Y": "Item ID",
        "Z": "Exception Required",
        "AA": "Exception For",
        "AB": "CSF Group",
        "AC": "Exception Duration - Start",
        "AD": "Exception Duration - End",
        "AE": "Impact to the Process",
        "AF": "Responsible",
        "AG": "Accountable",
        "AH": "Consulted",
        "AI": "Informed",
        "AJ": "Visibility",
        "AK": "Alerting",
        "AL": "Detection",
        "AM": "Telemetry",
        "AN": "Signals",
        "AO": "Components"
    },
    "NICE Framework": {
        "A": {
            "name": "Securely Provision",
            "provides": ["B", "C", "D", "E"]
        },
        "B": {
            "name": "Analyze",
            "involves": ["F", "G", "H"]
        },
        "C": {
            "name": "Collect and Operate",
            "involves": ["F", "I"]
        },
        "D": {
            "name": "Investigate",
            "involves": ["G", "H"]
        },
        "E": {
            "name": "Oversight and Development",
            "involves": ["I", "J", "K"]
        },
        "F": {
            "name": "Operate and Maintain",
            "involves": ["L", "K"]
        },
        "G": {
            "name": "Investigate",
            "involves": ["L", "M"]
        },
        "H": {
            "name": "Protect and Defend",
            "involves": ["K"]
        },
        "I": {
            "name": "Securely Provision",
            "provides": ["N"]
        },
        "J": {
            "name": "Analyze",
            "involves": ["N"]
        },
        "K": {
            "name": "Protect and Defend",
            "involves": ["N"]
        },
        "L": {
            "name": "Analyze",
            "involves": ["M"]
        },
        "M": {
            "name": "Collect and Operate",
            "involves": ["N"]
        },
        "N": {
            "name": "Operate and Maintain"
        }
    },
    "Trouble Ticket Mapping System": {
        "A": {
            "name": "User",
            "creates": ["B"]
        },
        "B": {
            "name": "Trouble Ticket",
            "assigned_to": ["C"],
            "resolves": ["D"]
        },
        "C": "Updates",
        "D": "Resolved"
    },
    "Primary Work Role ID Mapping": {
        "A": {
            "name": "Primary Work Role ID",
            "has": ["B", "C", "D", "E", "F", "G"]
        },
        "B": "Description",
        "C": "Email",
        "D": "Problem",
        "E": "Change",
        "F": "Request",
        "G": "Incident"
    },
    "ISO": {
        "A": {
            "name": "ISO",
            "maps_to": ["B"]
        },
        "B": "Securely Provision KSA"
    },
    "AO": {
        "A": {
            "name": "AO",
            "maps_to": ["B"]
        },
        "B": "Oversight and Development KSA"
    },
    "CIO": {
        "A": {
            "name": "CIO",
            "maps_to": ["B"]
        },
        "B": "Oversight and Development KSA"
    },
    "SCA": {
        "A": {
            "name": "SCA",
            "maps_to": ["B"]
        },
        "B": "Analyze KSA"
    },
    "SYS_ADMIN": {
        "A": {
            "name": "SYS_ADMIN",
            "maps_to": ["B"]
        },
        "B": "Operate and Maintain KSA"
    },
    "NET_ADMIN": {
        "A": {
            "name": "NET_ADMIN",
            "maps_to": ["B"]
        },
        "B": "Operate and Maintain KSA"
    },
    "DB_ADMIN": {
        "A": {
            "name": "DB_ADMIN",
            "maps_to": ["B"]
        },
        "B": "Operate and Maintain KSA"
    },
    "SEC_ARCH": {
        "A": {
            "name": "SEC_ARCH",
            "maps_to": ["B"]
        },
        "B": "Analyze KSA"
    },
    "APP_DEV": {
        "A": {
            "name": "APP_DEV",
            "maps_to": ["B"]
        },
        "B": "Analyze KSA"
    },
    "INC_RESP": {
        "A": {
            "name": "INC_RESP",
            "maps_to": ["B"]
        },
        "B": "Protect and Defend KSA"
    },
    "THREAT_ANALYST": {
        "A": {
            "name": "THREAT_ANALYST",
            "maps_to": ["B"]
        },
        "B": "Analyze KSA"
    }
}
