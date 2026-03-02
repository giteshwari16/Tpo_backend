TPO Portal Project Roadmap (ROADMAP.md)
Project Goal
Build a full-stack Training & Placement Office (TPO) portal for R. C. Patel IMRD, featuring a student dashboard, admin panel, placement prep resources, and an ML-driven fatigue analyzer.

Phase 1: Environment & Foundation
[ ] Backend Setup: Initialize Django project in /backend. Install DRF, SimpleJWT, and CORS headers.

[ ] Frontend Setup: Initialize Bootstrap 5 structure in /frontend.

[ ] Auth System: Create custom User model (Email-based) with is_admin and is_student roles.

[ ] Branding: Implement header/footer matching the college website image (Navy Blue #1a237e / White / Light Blue).

Phase 2: Database & Core Models
[ ] Models: Define StudentProfile, JobProfile, PrepMaterial, and FatigueLog.

[ ] Admin Customization: Customize Django Admin to manage students, jobs, and view fatigue trends.

[ ] Data Seeding: Create seed_data.json with 100+ questions and run loaddata.

Phase 3: Dashboard & Features
[ ] Sidebar & Navigation: Build the fixed right-list sidebar with dropdowns for Technical Prep categories.

[ ] Job Board: Create the interactive job listing UI connected to /api/jobs/.

[ ] Prep Sections: Build the dynamic question-answer UI for Aptitude and Technical sections.

Phase 4: ML Fatigue Analyzer (The "Brain")
[ ] Logic: Implement the heuristic fatigue calculation in views.py.

[ ] UI: Create the 'Daily Wellness Logger' form and the Chart.js Gauge Meter.

[ ] Recommender: Link fatigue levels to study schedule recommendations (e.g., High Fatigue → Suggest "HR Interview Prep").

Phase 5: Final Integration & Testing
[ ] JWT Integration: Secure all private routes with the JWT token flow.

[ ] Mobile Optimization: Test and fix all Bootstrap breakpoints for mobile view.

[ ] Handover: Create a README.md with instructions on how to run the project.
