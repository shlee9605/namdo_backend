import random
from sqlalchemy.sql import exists

from libs.hashUtil import hashPassword
from models.users import Users
from models.facility import Facility
from models.process import Process
from models.plan import Plan 
from models.bom import BOM
from models.gant import Gant
from models.achievement import Achievement

async def input_test_data(session):
    test_user = session.query(
        exists().where(Users.id == 1)
    ).scalar()
    if not test_user:
        await add_test_user_data(session)

    test_facility = session.query(
        exists().where(Facility.id == 1)
    ).scalar()
    if not test_facility:
        await add_test_facility_data(session)

    test_process = session.query(
        exists().where(Process.id == 1)
        ).scalar()
    if not test_process:
        await add_test_process_data(session)
        
    test_plan = session.query(
        exists().where(Plan.id == 1)
    ).scalar()
    if not test_plan:
        await add_test_plan_data(session)
    
    test_bom = session.query(
        exists().where(BOM.id == 1)
    ).scalar()
    if not test_bom:
        await add_test_bom_data(session)

    test_gant = session.query(
        exists().where(Gant.id == 1)
    ).scalar()
    if not test_gant:
        await add_test_gant_data(session)

    test_achievement = session.query(
        exists().where(Achievement.id == 1)
    ).scalar()
    if not test_achievement:
        await add_test_achievement_data(session)

async def add_test_user_data(session):
    Master = Users(
        user_id="Master",
        pass_word=hashPassword("Master"),
        name="마스터",
        email="Master@Master.com",
        role="Master"
    )
    session.add(Master)

    Admin = Users(
        user_id="Admin",
        pass_word=hashPassword("Admin"),
        name="어드민",
        email="Admin@Admin.com",
        role="Admin"
    )
    session.add(Admin)

    Worker = Users(
        user_id="Worker",
        pass_word=hashPassword("Worker"),
        name="워커",
        email="Worker@Worker.com",
        role="Worker"
    )
    session.add(Worker)
    session.commit()

async def add_test_facility_data(session):
    Facility1 = Facility(
        facility_name = "MCT 1",
    )
    session.add(Facility1)

    Facility2 = Facility(
        facility_name = "MCT 2",
    )
    session.add(Facility2)

    Facility3 = Facility(
        facility_name = "MCT 3",
    )
    session.add(Facility3)
    
    Facility4 = Facility(
        facility_name = "CNC 1",
    )
    session.add(Facility4)
    
    Facility5 = Facility(
        facility_name = "CNC 2",
    )
    session.add(Facility5)
    
    Facility6 = Facility(
        facility_name = "CNC 3",
    )
    session.add(Facility6)
    session.commit()

async def add_test_process_data(session):
    Process1 = Process(
        process_name = "A-1",
    )
    session.add(Process1)

    Process2 = Process(
        process_name = "A-2",
    )
    session.add(Process2)

    Process3 = Process(
        process_name = "A-3",
    )
    session.add(Process3)

    Process4 = Process(
        process_name = "B-1",
    )
    session.add(Process4)

    Process5 = Process(
        process_name = "B-2",
    )
    session.add(Process5)

    Process6 = Process(
        process_name = "B-3",
    )
    session.add(Process6)

    session.commit()

async def add_test_plan_data(session):
    Plan1 = Plan(
        madedate="20230701",
        company="Alpha",
        product_name="AAA",
        product_unit="111",
        background_color="#{:02x}{:02x}{:02x}".format(random.randint(125, 255), random.randint(125, 255),
                                                      random.randint(125, 255)),
        amount=100,
        state="Editting",
        bom_state="Done",
    )
    session.add(Plan1)

    Plan2 = Plan(
        madedate="20230708",
        company="Bravo",
        product_name="BBB",
        product_unit="111",
        background_color="#{:02x}{:02x}{:02x}".format(random.randint(125, 255), random.randint(125, 255),
                                                      random.randint(125, 255)),
        amount=200,
        state="Editting",
        bom_state="Done",
    )
    session.add(Plan2)

    Plan3 = Plan(
        madedate="20230715",
        company="Charlie",
        product_name="CCC",
        product_unit="112",
        background_color="#{:02x}{:02x}{:02x}".format(random.randint(125, 255), random.randint(125, 255),
                                                      random.randint(125, 255)),
        amount=400,
        state="Editting",
        bom_state="Done",
    )
    session.add(Plan3)
    
    Plan4 = Plan(
        madedate="20230723",
        company="Delta",
        product_name="DDD",
        product_unit="120",
        background_color="#{:02x}{:02x}{:02x}".format(random.randint(125, 255), random.randint(125, 255),
                                                      random.randint(125, 255)),
        amount=800,
        bom_state="Editting",
    )
    session.add(Plan4)

    Plan5 = Plan(
        madedate="20230730",
        company="Echo",
        product_name="EEE",
        product_unit="120",
        background_color="#{:02x}{:02x}{:02x}".format(random.randint(125, 255), random.randint(125, 255),
                                                      random.randint(125, 255)),
        amount=1600,
    )
    session.add(Plan5)

    Plan6 = Plan(
        madedate="20230801",
        company="Foxtrot",
        product_name="FFF",
        product_unit="130",
        background_color="#{:02x}{:02x}{:02x}".format(random.randint(125, 255), random.randint(125, 255),
                                                      random.randint(125, 255)),
        amount=3200,
    )
    session.add(Plan6)
    
    session.commit()

async def add_test_bom_data(session):
    BOM1_1 = BOM(
        plan_id = 1,
        process_name = "A-1",
        process_order = 0,
    )
    session.add(BOM1_1)
    
    BOM1_2 = BOM(
        plan_id = 1,
        process_name = "A-2",
        process_order = 1,
    )
    session.add(BOM1_2)

    BOM1_3 = BOM(
        plan_id = 1,
        process_name = "A-3",
        process_order = 2,
    )
    session.add(BOM1_3)

    BOM2_4 = BOM(
        plan_id = 2,
        process_name = "A-1",
        process_order = 0,
    )
    session.add(BOM2_4)

    BOM2_5 = BOM(
        plan_id = 2,
        process_name = "A-2",
        process_order = 1,
    )
    session.add(BOM2_5)

    BOM2_6 = BOM(
        plan_id = 2,
        process_name = "A-1",
        process_order = 2,
    )
    session.add(BOM2_6)

    BOM2_7 = BOM(
        plan_id = 2,
        process_name = "A-3",
        process_order = 3,
    )
    session.add(BOM2_7)

    BOM3_8 = BOM(
        plan_id = 3,
        process_name = "B-1",
        process_order = 0,
    )
    session.add(BOM3_8)
    
    BOM3_9 = BOM(
        plan_id = 3,
        process_name = "B-2",
        process_order = 1,
    )
    session.add(BOM3_9)

    BOM4_10 = BOM(
        plan_id = 4,
        process_name = "B-1",
        process_order = 0,
    )
    session.add(BOM4_10)
    
    BOM4_11 = BOM(
        plan_id = 4,
        process_name = "B-2",
        process_order = 1,
    )
    session.add(BOM4_11)

    BOM4_12 = BOM(
        plan_id = 4,
        process_name = "B-1",
        process_order = 2,
    )
    session.add(BOM4_12)

    BOM4_13 = BOM(
        plan_id = 4,
        process_name = "B-2",
        process_order = 3,
    )
    session.add(BOM4_13)

    session.commit()

async def add_test_gant_data(session):
    Gant1_1_1 = Gant(
        bom_id = 1,
        start_date = "2023-07-01T01:00:00",
        end_date = "2023-07-03T01:00:00",
        facility_name = "MCT 1",
    )
    session.add(Gant1_1_1)

    Gant1_1_2 = Gant(
        bom_id = 1,
        start_date = "2023-07-01T01:00:00",
        end_date = "2023-07-02T01:00:00",
        facility_name = "MCT 2",
    )
    session.add(Gant1_1_2)

    Gant1_2_3 = Gant(
        bom_id = 2,
        start_date = "2023-07-04T01:00:00",
        end_date = "2023-07-06T01:00:00",
        facility_name = "CNC 1",
    )
    session.add(Gant1_2_3)

    Gant1_3_4 = Gant(
        bom_id = 3,
        start_date = "2023-07-08T01:00:00",
        end_date = "2023-07-10T01:00:00",
        facility_name = "MCT 1",
    )
    session.add(Gant1_3_4)

    Gant2_4_5 = Gant(
        bom_id = 4,
        start_date = "2023-07-08T01:00:00",
        end_date = "2023-07-09T01:00:00",
        facility_name = "MCT 1",
    )
    session.add(Gant2_4_5)

    Gant2_4_6 = Gant(
        bom_id = 4,
        start_date = "2023-07-08T01:00:00",
        end_date = "2023-07-10T01:00:00",
        facility_name = "MCT 2",
    )
    session.add(Gant2_4_6)

    Gant2_5_7 = Gant(
        bom_id = 5,
        start_date = "2023-07-10T01:00:00",
        end_date = "2023-07-11T01:00:00",
        facility_name = "CNC 1",
    )
    session.add(Gant2_5_7)

    Gant2_6_8 = Gant(
        bom_id = 6,
        start_date = "2023-07-13T01:00:00",
        end_date = "2023-07-16T01:00:00",
        facility_name = "MCT 1",
    )
    session.add(Gant2_6_8)

    Gant2_6_9 = Gant(
        bom_id = 6,
        start_date = "2023-07-13T01:00:00",
        end_date = "2023-07-16T01:00:00",
        facility_name = "MCT 2",
    )
    session.add(Gant2_6_9)

    Gant2_7_10 = Gant(
        bom_id = 7,
        start_date = "2023-07-17T01:00:00",
        end_date = "2023-07-18T01:00:00",
        facility_name = "CNC 1",
    )
    session.add(Gant2_7_10)

    Gant2_7_11 = Gant(
        bom_id = 7,
        start_date = "2023-07-17T01:00:00",
        end_date = "2023-07-18T01:00:00",
        facility_name = "CNC 2",
    )
    session.add(Gant2_7_11)

    Gant3_8_12 = Gant(
        bom_id = 8,
        start_date = "2023-07-17T01:00:00",
        end_date = "2023-07-18T01:00:00",
        facility_name = "MCT 3",
    )
    session.add(Gant3_8_12)
    
    session.commit()

async def add_test_achievement_data(session):
    # Achievement1_1_1_1 = Achievement(
    #     gant_id = 1,
    #     user_name = "마스터",
    #     accomplishment = 30,
    # )
    # session.add(Achievement1_1_1_1)

    session.commit()