import mysql.connector
import random
from faker import Faker
import os

fake = Faker()

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123',             # <-- your MySQL root password
        database='PrisonManagement' # <-- matches your CREATE DATABASE
    )

def run_schema(cursor):
    # 1) figure out where generate.py lives
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 2) form the path to PrisonManagement_schema.sql in the same folder
    schema_file = os.path.join(script_dir, 'PrisonManagement_schema.sql')

    if not os.path.exists(schema_file):
        raise FileNotFoundError(
            f"Schema file not found at {schema_file!r}. "
            "Make sure PrisonManagement_schema.sql sits next to generate.py"
        )

    # 3) read & execute
    with open(schema_file, 'r') as f:
        stmts = [s.strip() for s in f.read().split(';') if s.strip()]
    for stmt in stmts:
        cursor.execute(stmt + ';')

def generate_guards(cursor, conn, num=2000):
    ranks = {
        'Warden': 10,
        'Sergeant': 100,
        'Lieutenant': 200,
        'Captain': 200,
        'Correctional Officer': int(num * 0.3),
        'Guard': num - 10 - 100 - 200 - 200 - int(num * 0.3)
    }
    shifts = ["Morning", "Day", "Night", "Rotating"]
    gid = 1
    for rank, count in ranks.items():
        for _ in range(count):
            name = f"{fake.first_name()} {fake.last_name()}"
            shift = random.choice(shifts)
            cursor.execute(
                "INSERT INTO Guard (GuardID, Name, `Rank`, ShiftSchedule) VALUES (%s, %s, %s, %s)",
                (gid, name, rank, shift)
            )
            gid += 1
            if gid > num:
                break
    conn.commit()

def generate_cells(cursor, conn, num=5000):
    levels = ["Low", "Medium", "High"]
    # pull existing guards for FK
    cursor.execute("SELECT GuardID FROM Guard")
    guards = [r[0] for r in cursor.fetchall()]

    for cid in range(1, num+1):
        guard_fk = random.choice(guards) if random.random() < 0.7 else None
        cursor.execute(
            "INSERT INTO Cell (CellID, BlockNumber, MaxOccupancy, SecurityLevel, GuardInCharge) "
            "VALUES (%s,%s,%s,%s,%s)",
            (cid, f"Block-{random.randint(1,50)}", random.randint(1,4),
             random.choice(levels), guard_fk)
        )
    conn.commit()

def generate_rehab_programs(cursor, conn, num=50):
    types = ['Educational','Vocational','Psychological','Substance Abuse','Life Skills']
    therapies = ['One-on-One','Group','Online']
    jobs = ['Auto Repair','Welding','Culinary Arts','Computer Skills']
    for rid in range(1, num+1):
        t = random.choice(types)
        name = fake.word().title() + " Program"
        therapy = random.choice(therapies) if t in ('Psychological','Substance Abuse') else None
        job = random.choice(jobs)    if t in ('Vocational','Life Skills')       else None
        rate = round(random.uniform(30,95),2)
        cursor.execute(
            "INSERT INTO Rehab (RehabID, Name, Type, Therapy, JobTraining, SuccessRate) "
            "VALUES (%s,%s,%s,%s,%s,%s)",
            (rid, name, t, therapy, job, rate)
        )
    conn.commit()

def generate_staff(cursor, conn, num=1000):
    types = ['Guard','Doctor','EducationProfessional']
    roles_for = {
        'Guard':['Guard'],
        'Doctor':['Doctor','Nurse','Therapist'],
        'EducationProfessional':['Teacher','Counselor','Case Worker']
    }
    deps_for = {
        'Guard':['Security'],
        'Doctor':['Medical'],
        'EducationProfessional':['Education','Counseling']
    }

    # first insert everyone without a roommate
    for sid in range(1, num+1):
        st = random.choice(types)
        role = random.choice(roles_for[st])
        dept = random.choice(deps_for[st])
        cursor.execute(
            "INSERT INTO Staff (StaffID, Name, Role, Department, StaffType, RoommateID) "
            "VALUES (%s,%s,%s,%s,%s,%s)",
            (sid, fake.name(), role, dept, st, None)
        )

    # then assign ~30% as roommates
    all_ids = list(range(1, num+1))
    for _ in range(int(num*0.3)):
        a = random.choice(all_ids)
        b = random.choice([x for x in all_ids if x!=a])
        cursor.execute(
            "UPDATE Staff SET RoommateID=%s WHERE StaffID=%s",
            (b,a)
        )
    conn.commit()

def generate_lawyers(cursor, conn, num=2000):
    for lid in range(1, num+1):
        name = f"{fake.first_name()} {fake.last_name()}"
        phone = fake.numerify('###-###-####')
        fax   = fake.numerify('###-###-####')
        age   = random.randint(25,75)
        cursor.execute(
            "INSERT INTO Lawyer (LawyerID, Name, Age, PhoneNumber, FaxNumber) "
            "VALUES (%s,%s,%s,%s,%s)",
            (lid, name, age, phone, fax)
        )
    conn.commit()

def generate_inmates(cursor, conn, num=10000):
    # grab all PKs for FKs
    cursor.execute("SELECT CellID FROM Cell");        cells  = [r[0] for r in cursor]
    cursor.execute("SELECT GuardID FROM Guard");      guards = [r[0] for r in cursor]
    cursor.execute("SELECT StaffID FROM Staff");      staff  = [r[0] for r in cursor]
    cursor.execute("SELECT LawyerID FROM Lawyer");    laws   = [r[0] for r in cursor]
    cursor.execute("SELECT RehabID FROM Rehab");      rehabs = [r[0] for r in cursor]

    crimes = ['Theft','Assault','Fraud','Drug Possession','Burglary']
    behaviors = [
      'Good behavior, participates',
      'Follows rules, keeps to self',
      'Occasional outbursts',
      'Multiple disciplinary actions',
      'Contraband history',
      'Model prisoner'
    ]

    for iid in range(1, num+1):
        cursor.execute(
            """INSERT INTO Inmate
               (InmateID, Name, Age, CrimeCommitted, SentenceDuration,
                CellAssignment, GuardID, StaffID, LawyerID, RehabID, BehaviorRecord)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (
              iid,
              fake.name(),
              random.randint(18,80),
              random.choice(crimes),
              random.randint(1,25),
              random.choice(cells),
              random.choice(guards),
              random.choice(staff),
              random.choice(laws),
              random.choice(rehabs),
              random.choice(behaviors)
            )
        )
    conn.commit()

def generate_visitors(cursor, conn, num=50000):
    cursor.execute("SELECT InmateID FROM Inmate")
    inmates = [r[0] for r in cursor]

    rels = ['Parent','Sibling','Spouse','Friend','Legal Counsel']
    for vid in range(1, num+1):
        cursor.execute(
            "INSERT INTO Visitor (VisitorID, Name, RelationshipToInmate, InmateID) "
            "VALUES (%s,%s,%s,%s)",
            (vid, fake.name(), random.choice(rels), random.choice(inmates))
        )
    conn.commit()

def main():
    conn = connect_db()
    cursor = conn.cursor()

    # 1) rebuild schema
    run_schema(cursor)
    # 2) generate tables in correct order
    generate_guards(cursor, conn)
    generate_cells(cursor, conn)
    generate_rehab_programs(cursor, conn)
    generate_staff(cursor, conn)
    generate_lawyers(cursor, conn)
    generate_inmates(cursor, conn)
    generate_visitors(cursor, conn)

    # migrate the real guard assignments into the junction…
    cursor.execute("""
      INSERT INTO Inmate_Staff (InmateID, StaffID, AssignmentStart)
      SELECT i.InmateID, i.StaffID, CURDATE()
      FROM Inmate i
      JOIN Staff s ON i.StaffID = s.StaffID
      WHERE i.StaffID IS NOT NULL;
    """)
    # same for rehab and lawyer…
    cursor.execute("""
      INSERT INTO Inmate_RehabProgram (InmateID,RehabID,EnrollDate)
      SELECT InmateID,RehabID,CURDATE() FROM Inmate WHERE RehabID IS NOT NULL;
    """)
    cursor.execute("""
      INSERT INTO Inmate_Lawyer (InmateID,LawyerID,CaseStartDate)
      SELECT InmateID,LawyerID,CURDATE() FROM Inmate WHERE LawyerID IS NOT NULL;
    """)
    conn.commit()

    cursor.close()
    conn.close()

if __name__=='__main__':
    main()
