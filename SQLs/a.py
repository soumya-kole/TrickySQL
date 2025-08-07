
-- Patients Table
CREATE OR REPLACE TABLE patients (
    patient_id INTEGER PRIMARY KEY,
    first_name STRING,
    last_name STRING,
    dob DATE,
    gender STRING
);

INSERT INTO patients VALUES
(1, 'John', 'Doe', '1980-01-01', 'M'),
(2, 'Alice', 'Smith', '1992-07-15', 'F'),
(3, 'Robert', 'Brown', '1975-10-10', 'M');

-- Providers Table
CREATE OR REPLACE TABLE providers (
    provider_id INTEGER PRIMARY KEY,
    provider_name STRING,
    specialty STRING
);

INSERT INTO providers VALUES
(101, 'Dr. Adams', 'Cardiology'),
(102, 'Dr. Baker', 'Pediatrics');

-- Claims Table
CREATE OR REPLACE TABLE claims (
    claim_id INTEGER PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id),
    provider_id INTEGER REFERENCES providers(provider_id),
    visit_id INTEGER REFERENCES visits(visit_id),  -- Optional
    claim_date DATE,
    claim_amount FLOAT,
    settlement_date DATE,
    settlement_amount FLOAT
);

INSERT INTO claims VALUES
(1001, 1, 101, NULL, '2023-01-15', 1200.00, '2023-01-25', 1100.00),
(1002, 2, 102, NULL, '2023-02-10', 800.00, '2023-02-20', 750.00),
(1003, 1, 101, NULL, '2023-03-05', 950.00, '2023-03-15', 920.00);

-- Visits Table
CREATE OR REPLACE TABLE visits (
    visit_id INTEGER PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id),
    provider_id INTEGER REFERENCES providers(provider_id),
    visit_date DATE,
    reason STRING,
    billed_amount FLOAT,
    claim_id INTEGER REFERENCES claims(claim_id)  -- New relationship
);

INSERT INTO visits VALUES
(401, 1, 101, '2023-01-15', 'Annual Checkup', NULL, NULL),
(402, 2, 102, '2023-02-10', 'Cough', 800.00, 1002),
(403, 3, 101, '2023-03-20', 'Follow-up', 980.00, NULL);

-- Diagnoses Table
CREATE OR REPLACE TABLE diagnoses (
    diagnosis_id INTEGER PRIMARY KEY,
    claim_id INTEGER REFERENCES claims(claim_id),
    diagnosis_code STRING,
    description STRING
);

INSERT INTO diagnoses VALUES
(201, 1001, 'I10', 'Hypertension'),
(202, 1002, 'J45', 'Asthma'),
(203, 1003, 'E11', 'Type 2 Diabetes');

-- Medications Table
CREATE OR REPLACE TABLE medications (
    medication_id INTEGER PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id),
    medication_name STRING,
    start_date DATE,
    end_date DATE
);

INSERT INTO medications VALUES
(301, 1, 'Lisinopril', '2023-01-16', '2023-07-16'),
(302, 2, 'Albuterol', '2023-02-12', '2023-08-12'),
(303, 3, 'Metformin', '2023-04-01', '2023-10-01');


1. patients
Stores demographic details of individuals receiving care.

Column	Type	Description
patient_id	INTEGER	Primary key. Unique ID for each patient.
first_name	STRING	Patient’s first name.
last_name	STRING	Patient’s last name.
dob	DATE	Date of birth of the patient.
gender	STRING	Gender of the patient ('M' = Male, 'F' = Female).

2. providers
Stores data about healthcare professionals providing services.

Column	Type	Description
provider_id	INTEGER	Primary key. Unique ID for the provider.
provider_name	STRING	Name of the provider (e.g., "Dr. Adams").
specialty	STRING	Medical specialty (e.g., "Cardiology").

3. visits
Represents patient visits to providers. Some visits may not be billed or claimed.

Column	Type	Description
visit_id	INTEGER	Primary key. Unique ID for each visit.
patient_id	INTEGER	Foreign key → patients.patient_id.
provider_id	INTEGER	Foreign key → providers.provider_id.
visit_date	DATE	Date of the visit.
reason	STRING	Visit reason (e.g., "Checkup", "Follow-up").
billed_amount	FLOAT	Amount billed in US dollars (e.g., 980.00). Can be NULL if no billing.
claim_id	INTEGER	Optional foreign key → claims.claim_id. Links to a claim if one exists.

4. claims
Insurance claims submitted for reimbursement. Not all visits result in claims.

Column	Type	Description
claim_id	INTEGER	Primary key. Unique ID for each claim.
patient_id	INTEGER	Foreign key → patients.patient_id. Patient who filed the claim.
provider_id	INTEGER	Foreign key → providers.provider_id. Provider rendering the service.
visit_id	INTEGER	Optional foreign key → visits.visit_id. Originating visit, if available.
claim_date	DATE	Date the claim was submitted.
claim_amount	FLOAT	Amount claimed in US dollars (e.g., 1200.00).
settlement_date	DATE	Date claim was processed and settled.
settlement_amount	FLOAT	Final amount paid by insurance in USD (e.g., 1100.00).

5. diagnoses
Diagnoses associated with submitted claims.

Column	Type	Description
diagnosis_id	INTEGER	Primary key. Unique ID for the diagnosis record.
claim_id	INTEGER	Foreign key → claims.claim_id. Associated with a specific claim.
diagnosis_code	STRING	ICD-10 diagnosis code (e.g., 'I10' for Hypertension).
description	STRING	Description of the diagnosis.

6. medications
Medication history for patients.

Column	Type	Description
medication_id	INTEGER	Primary key. Unique ID for each medication record.
patient_id	INTEGER	Foreign key → patients.patient_id. Patient prescribed the drug.
medication_name	STRING	Name of the medication (e.g., "Metformin").
start_date	DATE	Start date of the medication.
end_date	DATE	End date of the medication (can be in future if ongoing).

🔗 ENTITY RELATIONSHIPS
css
Copy
Edit
[patients] 1 ────< [visits] >──── 1 [providers]
     │         ▲         │
     │         │         └────< [claims] >──── 1 [diagnoses]
     │         └──────────────────────────────┘
     └───────────────< [medications]
⚙️ Relationship Notes:
One patient can have many visits, claims, diagnoses, and medications.

One provider can attend many visits and be referenced in many claims.

One visit can optionally generate one claim.

One claim can optionally be linked to one visit.

One claim can have many diagnoses.

Billing and claims are optional (not all visits are billed or reimbursed).
