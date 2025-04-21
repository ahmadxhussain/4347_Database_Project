import mysql.connector
import random
from faker import Faker
import os
from datetime import date, timedelta

fake = Faker()

def connect_db():
    """Connect to the MySQL database."""
    return mysql.connector.connect(
        host='localhost',     # or your MySQL host
        user='root',          # your MySQL user
        password='123',       # your MySQL password
        database='PrisonDB'   # your database
    )

def run_schema(cursor):
    """Execute schema SQL from file to recreate tables."""
    # Path to your schema file
    schema_file = '/Users/ahmadhussain/documents/4347 Database/project part 2/PrisonDB_schema.sql'

    # Ensure the file exists
    if not os.path.exists(schema_file):
        raise FileNotFoundError(f"Schema file not found: {schema_file}")

    # Open and execute the schema file
    with open(schema_file, 'r') as f:
        sql_statements = f.read().split(';')
    for stmt in sql_statements:
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt + ';')


def generate_cells(cursor, conn, num=5000):
    for cell_id in range(1, num+1):
        cursor.execute(
            "INSERT INTO Cells (CellID, BlockNumber, MaxOccupancy, SecurityLevel) VALUES (%s, %s, %s, %s)",
            (cell_id,
             random.randint(1,50),
             random.randint(1,4),
             random.choice([1,2,3])  # assuming 1=Low,2=Medium,3=High
            )
        )
    conn.commit()

def generate_guards(cursor, conn, num=2000):
    # Define guard ranks and their quantities
    ranks = {
        'Warden': 10,
        'Sergeant': 100,
        'Lieutenant': 200,
        'Captain': 200,
        'Correctional Officer': int(num * 0.3),  # 30% of total
        'Guard': num - 10 - 100 - 200 - 200 - int(num * 0.3)  # Remaining guards
    }

    # Define shift schedules
    shift_schedules = ["Morning", "Day", "Night", "Rotating"]

    guard_id = 1
    for rank, count in ranks.items():
        for _ in range(count):
            # Generate clean names without titles
            first_name = fake.first_name()
            last_name = fake.last_name()
            full_name = f"{first_name} {last_name}"

            # Assign a random shift schedule
            shift = random.choice(shift_schedules)

            # Most guards won't be assigned to a specific cell, only some
            cell_id = None
            if random.random() < 0.3:  # 30% chance to be assigned to a cell
                # This assumes you have cells with IDs from 1 to 500
                # Adjust the range based on your actual cell IDs
                cell_id = random.randint(1, 500)

            cursor.execute(
                "INSERT INTO Guards (GuardID, Name, `Rank`, ShiftSchedule, CellID) VALUES (%s, %s, %s, %s, %s)",
                (guard_id, full_name, rank, shift, cell_id)
            )

            guard_id += 1

            # Safety check to avoid exceeding the total
            if guard_id > num:
                break

    conn.commit()





def generate_rehab_programs(cursor, conn, num=50):
    for program_id in range(1, num + 1):
        # Generate program names and types
        rehab_types = ['Educational', 'Vocational', 'Psychological', 'Substance Abuse', 'Life Skills']
        rehab_type = random.choice(rehab_types)

        # Create program name based on type
        if rehab_type == 'Educational':
            names = ['Basic Education', 'GED Preparation', 'College Courses', 'Literacy Program',
                     'Mathematics Skills', 'Computer Literacy', 'History Studies', 'Science Education']
        elif rehab_type == 'Vocational':
            names = ['Carpentry', 'Plumbing', 'Electrical Work', 'Culinary Arts', 'Auto Repair',
                     'Welding', 'HVAC Training', 'Cosmetology', 'Landscaping', 'Masonry']
        elif rehab_type == 'Psychological':
            names = ['Anger Management', 'Cognitive Behavioral Therapy', 'Trauma Counseling',
                     'Conflict Resolution', 'Family Therapy', 'Emotional Intelligence', 'Stress Management']
        elif rehab_type == 'Substance Abuse':
            names = ['Narcotics Anonymous', 'Alcoholics Anonymous', 'Drug Rehabilitation',
                     'Substance Counseling', 'Addiction Recovery', 'Sobriety Support']
        else:  # Life Skills
            names = ['Financial Management', 'Parenting Skills', 'Job Interview Preparation',
                     'Resume Building', 'Communication Skills', 'Health and Wellness', 'Decision Making']

        program_name = random.choice(names)

        # Generate a success rate based on program type
        if rehab_type in ['Educational', 'Vocational']:
            success_rate = round(random.uniform(60, 95), 2)
        elif rehab_type == 'Psychological':
            success_rate = round(random.uniform(40, 85), 2)
        elif rehab_type == 'Substance Abuse':
            success_rate = round(random.uniform(30, 75), 2)
        else:  # Life Skills
            success_rate = round(random.uniform(50, 90), 2)

        # Insert into the RehabPrograms table - CORRECTED TABLE NAME
        cursor.execute(
            "INSERT INTO RehabPrograms (ProgramID, Name, RehabType, SuccessRate) VALUES (%s, %s, %s, %s)",
            (program_id, program_name, rehab_type, success_rate)
        )

    conn.commit()



def generate_staff(cursor, conn, num=1000):
    roles = ['Doctor','Counselor','Case Worker','Therapist']
    deps  = ['Medical','Counseling','Admin']
    types = ['Full-Time','Part-Time']
    for sid in range(1, num+1):
        cursor.execute(
            "INSERT INTO Staff (EmployeeID, Name, Role, Department, StaffType) VALUES (%s, %s, %s, %s, %s)",
            (sid, fake.name(), random.choice(roles), random.choice(deps), random.choice(types))
        )
    conn.commit()

def generate_lawyers(cursor, conn, num=2000):
    for lid in range(1, num + 1):
        # Generate clean names without titles
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"

        # Generate shorter phone numbers with a consistent format
        phone = fake.numerify('###-###-####')
        fax = fake.numerify('###-###-####')

        cursor.execute(
            "INSERT INTO Lawyers (LawyerID, Name, Age, PhoneNumber, FaxNumber) VALUES (%s, %s, %s, %s, %s)",
            (lid, full_name, random.randint(25, 75), phone, fax)
        )
    conn.commit()



def generate_inmates(cursor, conn, num=10000):
    crimes = ['Theft','Assault','Fraud','Drug Possession','Burglary']
    for iid in range(1, num+1):
        cursor.execute(
            "INSERT INTO Inmates (InmateID, Name, Age, Crime, SentenceYears, CellID, GuardID, BehaviorRecord) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (iid, fake.name(), random.randint(18,80),
             random.choice(crimes), round(random.uniform(1,20),1),
             random.randint(1,5000), random.randint(1,2000),
             random.choice(['Good','Neutral','Poor']))
        )
    conn.commit()

def generate_visitors(cursor, conn, num=50000):
    statuses = ['Approved','Denied','Pending']
    for vid in range(1, num+1):
        visit_date = fake.date_between(start_date='-1y', end_date='today')
        cursor.execute(
            "INSERT INTO Visitors (VisitorID, InmateID, Name, Relationship, VisitDate, ApprovalStatus) VALUES (%s, %s, %s, %s, %s, %s)",
            (vid, random.randint(1,10000), fake.name(),
             random.choice(['Family','Friend','Lawyer']),
             visit_date, random.choice(statuses))
        )
    conn.commit()

def generate_relationships(cursor, conn):
    # Lawyer_Inmate
    for _ in range(15000):
        cursor.execute("INSERT IGNORE INTO Lawyer_Inmate (LawyerID, InmateID) VALUES (%s, %s)",
                       (random.randint(1,2000), random.randint(1,10000)))
    # Staff_Inmate
    for _ in range(10000):
        cursor.execute("INSERT IGNORE INTO Staff_Inmate (EmployeeID, InmateID) VALUES (%s, %s)",
                       (random.randint(1,1000), random.randint(1,10000)))
    # Inmate_Rehab
    for _ in range(5000):
        cursor.execute("INSERT IGNORE INTO Inmate_Rehab (InmateID, ProgramID) VALUES (%s, %s)",
                       (random.randint(1,10000), random.randint(1,25)))
    # Lawyer_Staff
    for _ in range(5000):
        cursor.execute("INSERT IGNORE INTO Lawyer_Staff (LawyerID, EmployeeID) VALUES (%s, %s)",
                       (random.randint(1,2000), random.randint(1,1000)))
    conn.commit()

def main():
    conn = connect_db()
    cursor = conn.cursor()
    run_schema(cursor)
    generate_cells(cursor, conn)
    generate_guards(cursor, conn)
    generate_rehab_programs(cursor, conn)
    generate_staff(cursor, conn)
    generate_lawyers(cursor, conn)
    generate_inmates(cursor, conn)
    generate_visitors(cursor, conn)
    generate_relationships(cursor, conn)
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
