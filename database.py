"""
Database Management Module.
Handles SQLite schema, connection pooling, and initial seed data for students, resources, and feedback.
"""

import sqlite3
import os
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), "learning_system.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Students Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        age INTEGER DEFAULT 20,
        semester TEXT DEFAULT 'Semester 4',
        cgpa REAL DEFAULT 7.5,
        preferred_subject TEXT DEFAULT 'Programming',
        learning_style TEXT DEFAULT 'Visual',
        skill_level TEXT DEFAULT 'Intermediate',
        study_hours REAL DEFAULT 5.0,
        attendance REAL DEFAULT 82.0,
        previous_score REAL DEFAULT 72.0,
        assignment_score REAL DEFAULT 75.0,
        quiz_score REAL DEFAULT 70.0,
        weak_topic TEXT DEFAULT 'Pointers & Dynamic Memory',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Resources Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        topic TEXT NOT NULL,
        resource_type TEXT NOT NULL, -- Video, Notes, Practice, Projects, Books, Articles, Tutorials
        difficulty TEXT NOT NULL,    -- Beginner, Intermediate, Advanced
        description TEXT,
        duration TEXT,
        url TEXT DEFAULT '#',
        rating REAL DEFAULT 4.5
    );
    """)

    # 3. Feedback Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        resource_id INTEGER,
        resource_title TEXT NOT NULL,
        rating INTEGER NOT NULL,     -- 1 to 5
        is_useful INTEGER DEFAULT 1, -- 1 for Yes, 0 for No
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 4. Admins Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT DEFAULT 'System Administrator'
    );
    """)

    # Seed Admin if not exists
    cursor.execute("SELECT id FROM admins WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admins (username, password, name) VALUES (?, ?, ?)",
                       ("admin", hash_pw("admin123"), "Lead Administrator"))

    # Seed Sample Students if empty
    cursor.execute("SELECT COUNT(*) as count FROM students")
    if cursor.fetchone()["count"] == 0:
        demo_students = [
            ("S001", "Suman Jana", "suman@example.com", hash_pw("student123"), 21, "Semester 5", 8.4,
             "Programming", "Visual", "Intermediate", 6.0, 88.0, 78.0, 82.0, 75.0, "Graph Algorithms"),
            ("S002", "Priya Sharma", "priya@example.com", hash_pw("student123"), 20, "Semester 4", 9.1,
             "Data Science", "Reading/Writing", "Advanced", 7.5, 95.0, 92.0, 94.0, 90.0, "Neural Networks"),
            ("S003", "Rahul Roy", "rahul@example.com", hash_pw("student123"), 22, "Semester 6", 6.2,
             "Web Development", "Kinesthetic", "Beginner", 3.0, 62.0, 48.0, 52.0, 45.0, "CSS Grid & Flexbox"),
            ("S004", "Ananya Das", "ananya@example.com", hash_pw("student123"), 20, "Semester 4", 7.8,
             "SQL & Databases", "Auditory", "Intermediate", 5.0, 80.0, 70.0, 74.0, 68.0, "Query Optimization"),
        ]
        cursor.executemany("""
        INSERT INTO students (student_id, name, email, password, age, semester, cgpa,
                              preferred_subject, learning_style, skill_level, study_hours,
                              attendance, previous_score, assignment_score, quiz_score, weak_topic)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, demo_students)

    # Seed Comprehensive Learning Resources
    cursor.execute("SELECT COUNT(*) as count FROM resources")
    if cursor.fetchone()["count"] == 0:
        demo_resources = [
            # Data Structures & Algorithms
            ("Graph Mastery: Complete BFS & DFS Video Guide", "Data Structures", "Video", "Intermediate", "Step-by-step visual animation of Graph Traversals with time complexity.", "1 hr 45 min", 4.9, "https://www.youtube.com/watch?v=pcKY4hjDrxk"),
            ("Interactive Graph Algorithm Visualizer", "Data Structures", "Practice", "Intermediate", "Web-based interactive sandbox to construct graphs and trace Dijkstra/Prim algorithms.", "45 min", 4.8, "https://visualgo.net/en/graphds"),
            ("Graph Theory & Tree Traversal Comprehensive Handbook", "Data Structures", "Notes", "Beginner", "Full summary notes with annotated diagrams and recurrence relations.", "28 pages", 4.7, "https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/"),
            ("Top 50 Graph & Tree Coding Challenges", "Data Structures", "Practice", "Advanced", "Curated LeetCode / Codeforces algorithmic problems with full test suites.", "40 problems", 4.9, "https://leetcode.com/problemset/all/?topicSlugs=graph%2Ctree"),
            ("Build a Route Planning Navigation Engine", "Data Structures", "Projects", "Advanced", "Implement Dijkstra & A* search in Python to calculate shortest paths on maps.", "2 days", 4.9, "https://github.com/topics/dijkstra-algorithm"),

            # Java OOP
            ("Java OOP In-Depth: Polymorphism & Interface Design", "Java", "Video", "Intermediate", "Detailed video lectures explaining OOP pillars, interfaces, and design patterns.", "3.5 hrs", 4.8, "https://www.youtube.com/watch?v=xk4_1vDrzzo"),
            ("Core Java & JVM Memory Architecture Cheat Sheet", "Java", "Notes", "Beginner", "Pointers, Heap vs Stack memory, Garbage Collection, and Collections overview.", "22 pages", 4.6, "https://www.geeksforgeeks.org/jvm-works-jvm-architecture/"),
            ("100 Solved Java OOP Interview & Logic Questions", "Java", "Practice", "Intermediate", "Practice set focusing on encapsulation, exceptions, and multi-threading.", "35 exercises", 4.7, "https://www.javatpoint.com/core-java-interview-questions"),
            ("Mini Project: Multi-User Library Management System in Java", "Java", "Projects", "Intermediate", "Desktop CRUD application with Swing / JavaFX and SQLite database.", "3 days", 4.8, "https://github.com/topics/library-management-system-java"),

            # Python & Data Science
            ("Pandas & NumPy for Exploratory Data Science", "Data Science", "Video", "Beginner", "High-yield video series on data wrangling, cleaning, and aggregation.", "4 hrs", 4.9, "https://www.youtube.com/watch?v=vmEHCJofslg"),
            ("Statistical Foundations & Exploratory Analysis Manual", "Data Science", "Notes", "Intermediate", "Comprehensive guide on distributions, hypothesis testing, and regressions.", "34 pages", 4.7, "https://www.kaggle.com/learn/pandas"),
            ("Real-World Data Cleaning Drills (Kaggle Benchmark)", "Data Science", "Practice", "Intermediate", "Hands-on messy dataset exercises with missing value imputations.", "25 exercises", 4.8, "https://www.kaggle.com/learn/data-cleaning"),
            ("End-to-End Student Retention Predictive Analytics", "Data Science", "Projects", "Advanced", "Complete machine learning pipeline with scikit-learn and Streamlit/Flask UI.", "4 days", 4.9, "https://github.com/topics/student-performance-prediction"),

            # Web Development
            ("Modern Responsive Frontend: HTML5, Modern CSS & JS", "Web Development", "Video", "Beginner", "Complete full-stack introductory walkthrough to build modern responsive websites.", "5 hrs", 4.8, "https://www.youtube.com/watch?v=mU6anWqZJcc"),
            ("Modern CSS Grid, Flexbox & DOM API Handbook", "Web Development", "Notes", "Beginner", "Concise visual cheat sheets and layout design best practices.", "18 pages", 4.6, "https://css-tricks.com/snippets/css/a-guide-to-flexbox/"),
            ("Frontend UI Challenges: Build 10 Interactive Web Components", "Web Development", "Practice", "Intermediate", "Drills covering modals, accordions, dynamic sliders, and AJAX fetch.", "10 challenges", 4.7, "https://www.frontendmentor.io/challenges"),
            ("Build a Real-Time Collaborative Task Dashboard", "Web Development", "Projects", "Intermediate", "Frontend application with local storage, dark mode, and drag-and-drop cards.", "3 days", 4.8, "https://github.com/topics/task-management-dashboard"),

            # SQL & Databases
            ("SQL Mastery: Joins, Subqueries & Window Functions", "SQL & Databases", "Video", "Intermediate", "Hands-on video tutorial covering advanced SQL querying patterns.", "3.5 hrs", 4.8, "https://www.youtube.com/watch?v=HXV3zeQKqGY"),
            ("Database Normalization (1NF to BCNF) & Indexing Notes", "SQL & Databases", "Notes", "Intermediate", "Theory and worked examples of database design and schema optimization.", "24 pages", 4.7, "https://www.geeksforgeeks.org/normal-forms-in-dbms/"),
            ("50 Benchmark SQL Queries for Data Analysts", "SQL & Databases", "Practice", "Intermediate", "Complex real-world grouping, aggregations, and CTE challenges.", "50 queries", 4.8, "https://leetcode.com/problemset/database/"),
            ("Design & Deploy an Enterprise Inventory Database", "SQL & Databases", "Projects", "Advanced", "Schema design, stored procedures, triggers, and relational constraints.", "3 days", 4.8, "https://github.com/topics/inventory-management-system-database"),

            # Computer Networks
            ("TCP/IP, OSI Layers & Packet Analysis Mastery", "Computer Networks", "Video", "Intermediate", "Visual packet tracing and protocol analysis using Wireshark.", "4 hrs", 4.7, "https://www.youtube.com/watch?v=IPvYjXCsTg8"),
            ("Subnetting, CIDR & Routing Protocols Quick Manual", "Computer Networks", "Notes", "Beginner", "Step-by-step mathematical subnet calculations and routing tables.", "20 pages", 4.6, "https://www.geeksforgeeks.org/ip-addressing-and-subnetting/"),
            ("IPv4/IPv6 Subnetting & Network Simulation Drills", "Computer Networks", "Practice", "Intermediate", "Problem sets covering IP addressing and subnet masks.", "30 exercises", 4.7, "https://www.subnetting.net/Subneting.aspx?mode=practice"),
            ("Simulate and Secure an Enterprise LAN in Packet Tracer", "Computer Networks", "Projects", "Advanced", "Full Cisco Packet Tracer topology with VLANs, DHCP, and firewall rules.", "2 days", 4.8, "https://www.packettracernetwork.com/tutorials/packet-tracer-tutorials.html"),

            # Programming Fundamentals (C)
            ("C Programming from Scratch: Pointers & Memory", "Programming Fundamentals (C)", "Video", "Beginner", "Master memory allocation (malloc/free), pointer arithmetic, and structs.", "5 hrs", 4.8, "https://www.youtube.com/watch?v=KJgsSFOSQv0"),
            ("C Control Structures, Arrays & Functions Summary", "Programming Fundamentals (C)", "Notes", "Beginner", "Syntax reference and algorithmic loop building patterns.", "22 pages", 4.6, "https://www.geeksforgeeks.org/c-programming-language/"),
            ("Logic Building & Pattern Printing 50 Exercises", "Programming Fundamentals (C)", "Practice", "Beginner", "Fundamental algorithmic drills to sharpen programming intuition.", "50 problems", 4.7, "https://www.geeksforgeeks.org/c-programs-to-print-number-pattern/"),
            ("Mini Project: Console Financial Ledger in C", "Programming Fundamentals (C)", "Projects", "Beginner", "File I/O operations, pointer data structures, and command-line menu.", "2 days", 4.7, "https://github.com/topics/c-projects")
        ]
        cursor.executemany("""
        INSERT INTO resources (title, topic, resource_type, difficulty, description, duration, rating, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, demo_resources)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at", DB_PATH)
