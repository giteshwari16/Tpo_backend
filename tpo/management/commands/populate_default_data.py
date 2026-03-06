from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tpo.models import JobProfile, Training

class Command(BaseCommand):
    help = 'Populate default job opportunities and training programs'

    def handle(self, *args, **options):
        # Clear existing data
        JobProfile.objects.all().delete()
        Training.objects.all().delete()
        
        # Create default job opportunities
        jobs = [
            {
                'company_name': 'TCS',
                'role': 'Software Developer',
                'category': 'IT',
                'ctc': '3.5 LPA',
                'eligibility': 'BE/B.Tech - 60% and above',
                'location': 'Mumbai, Pune, Bangalore',
                'deadline': timezone.now() + timedelta(days=15),
                'description': 'TCS is hiring Software Developers for their digital transformation projects. Candidates will work on cutting-edge technologies including AI, Cloud Computing, and Enterprise Applications. Strong programming skills in Java, Python, or C++ required. Knowledge of databases and web frameworks is preferred.'
            },
            {
                'company_name': 'Infosys',
                'role': 'Systems Engineer',
                'category': 'IT',
                'ctc': '3.2 LPA',
                'eligibility': 'BE/B.Tech - 65% and above',
                'location': 'Bangalore, Hyderabad, Chennai',
                'deadline': timezone.now() + timedelta(days=20),
                'description': 'Infosys is looking for Systems Engineers to join their global delivery team. Work on enterprise software solutions, cloud platforms, and digital transformation initiatives. Strong analytical and problem-solving skills required.'
            },
            {
                'company_name': 'Wipro',
                'role': 'Project Engineer',
                'category': 'IT',
                'ctc': '3.0 LPA',
                'eligibility': 'BE/B.Tech - 60% and above',
                'location': 'Pune, Bangalore, Delhi',
                'deadline': timezone.now() + timedelta(days=12),
                'description': 'Wipro is hiring Project Engineers for their IT services division. Candidates will work on software development, testing, and implementation projects. Knowledge of programming languages and software development lifecycle is essential.'
            },
            {
                'company_name': 'HCL Technologies',
                'role': 'Software Engineer',
                'category': 'IT',
                'ctc': '3.3 LPA',
                'eligibility': 'BE/B.Tech - 62% and above',
                'location': 'Noida, Chennai, Bangalore',
                'deadline': timezone.now() + timedelta(days=18),
                'description': 'HCL Technologies is recruiting Software Engineers for their engineering services division. Work on innovative solutions for clients across various industries. Strong foundation in computer science and programming required.'
            },
            {
                'company_name': 'Capgemini',
                'role': 'Associate Consultant',
                'category': 'Consulting',
                'ctc': '3.8 LPA',
                'eligibility': 'BE/B.Tech - 65% and above',
                'location': 'Mumbai, Bangalore, Delhi',
                'deadline': timezone.now() + timedelta(days=25),
                'description': 'Capgemini is hiring Associate Consultants for their consulting practice. Work with global clients on digital transformation, cloud migration, and business process optimization. Excellent communication and analytical skills required.'
            },
            {
                'company_name': 'Accenture',
                'role': 'Software Engineering Analyst',
                'category': 'Consulting',
                'ctc': '4.0 LPA',
                'eligibility': 'BE/B.Tech - 70% and above',
                'location': 'Mumbai, Bangalore, Hyderabad',
                'deadline': timezone.now() + timedelta(days=22),
                'description': 'Accenture is looking for Software Engineering Analysts to join their technology consulting team. Work on cutting-edge projects in cloud, AI, and digital transformation. Strong technical skills and business acumen required.'
            },
            {
                'company_name': 'Microsoft',
                'role': 'Software Engineer',
                'category': 'Product',
                'ctc': '12.0 LPA',
                'eligibility': 'BE/B.Tech - 75% and above, No backlogs',
                'location': 'Hyderabad, Bangalore',
                'deadline': timezone.now() + timedelta(days=30),
                'description': 'Microsoft is hiring Software Engineers for their product development teams. Work on world-class products including Windows, Office, Azure, and more. Exceptional programming skills and passion for technology required.'
            },
            {
                'company_name': 'Google',
                'role': 'Software Engineer',
                'category': 'Product',
                'ctc': '15.0 LPA',
                'eligibility': 'BE/B.Tech - 80% and above, No backlogs',
                'location': 'Bangalore, Hyderabad',
                'deadline': timezone.now() + timedelta(days=35),
                'description': 'Google is looking for talented Software Engineers to join their engineering teams. Work on products used by billions of users worldwide. Strong foundation in algorithms, data structures, and system design required.'
            },
            {
                'company_name': 'Amazon',
                'role': 'Software Development Engineer',
                'category': 'Product',
                'ctc': '14.0 LPA',
                'eligibility': 'BE/B.Tech - 75% and above, No backlogs',
                'location': 'Bangalore, Hyderabad, Delhi',
                'deadline': timezone.now() + timedelta(days=28),
                'description': 'Amazon is hiring Software Development Engineers for their technology teams. Work on AWS, e-commerce platforms, and innovative consumer products. Strong problem-solving skills and customer obsession required.'
            },
            {
                'company_name': 'L&T Infotech',
                'role': 'Software Engineer',
                'category': 'IT',
                'ctc': '3.4 LPA',
                'eligibility': 'BE/B.Tech - 60% and above',
                'location': 'Mumbai, Chennai, Bangalore',
                'deadline': timezone.now() + timedelta(days=16),
                'description': 'L&T Infotech is hiring Software Engineers for their IT services division. Work on enterprise applications, cloud solutions, and digital transformation projects. Knowledge of modern technologies and frameworks preferred.'
            }
        ]

        # Create job instances
        created_jobs = []
        for job_data in jobs:
            job = JobProfile.objects.create(**job_data)
            created_jobs.append(job)
            self.stdout.write(
                self.style.SUCCESS(f'Created job: {job.company_name} - {job.role}')
            )

        # Create default training programs
        trainings = [
            {
                'title': 'Full Stack Web Development Bootcamp',
                'description': 'Comprehensive training on modern web development technologies including HTML5, CSS3, JavaScript, React, Node.js, and MongoDB. Learn to build complete web applications from scratch. Includes hands-on projects and real-world scenarios.',
                'training_type': 'technical',
                'instructor': 'Tech Academy',
                'venue': 'Computer Lab - Block A',
                'start_date': timezone.now() + timedelta(days=3),
                'end_date': timezone.now() + timedelta(days=10),
                'duration_hours': 40,
                'capacity': 30,
                'is_online': False,
                'prerequisites': 'Basic programming knowledge, HTML/CSS fundamentals',
                'learning_outcomes': 'Build responsive web applications, understand frontend and backend development, work with databases, deploy applications to cloud platforms'
            },
            {
                'title': 'Data Science and Machine Learning',
                'description': 'Learn data science fundamentals, machine learning algorithms, data visualization, and predictive modeling. Work with Python libraries like NumPy, Pandas, Scikit-learn, and TensorFlow. Includes real-world datasets and case studies.',
                'training_type': 'technical',
                'instructor': 'Data Science Institute',
                'venue': 'Online - Zoom Meeting',
                'start_date': timezone.now() + timedelta(days=5),
                'end_date': timezone.now() + timedelta(days=12),
                'duration_hours': 35,
                'capacity': 50,
                'is_online': True,
                'meeting_link': 'https://zoom.us/j/1234567890',
                'prerequisites': 'Python programming, basic statistics, mathematics fundamentals',
                'learning_outcomes': 'Analyze datasets, build machine learning models, create data visualizations, understand ML algorithms and applications'
            },
            {
                'title': 'Aptitude and Logical Reasoning Mastery',
                'description': 'Master quantitative aptitude, logical reasoning, verbal ability, and problem-solving skills essential for campus placements. Practice with previous year questions and learn time-saving techniques.',
                'training_type': 'aptitude',
                'instructor': 'Placement Prep Experts',
                'venue': 'Seminar Hall - Block B',
                'start_date': timezone.now() + timedelta(days=2),
                'end_date': timezone.now() + timedelta(days=4),
                'duration_hours': 24,
                'capacity': 60,
                'is_online': False,
                'prerequisites': 'Basic mathematics, logical thinking ability',
                'learning_outcomes': 'Solve aptitude problems quickly, improve logical reasoning, master time management for exams, crack placement tests'
            },
            {
                'title': 'Communication Skills and Personality Development',
                'description': 'Enhance your communication skills, presentation abilities, interview techniques, and overall personality. Learn corporate etiquette, teamwork, and leadership skills through interactive sessions.',
                'training_type': 'soft_skills',
                'instructor': 'Soft Skills Academy',
                'venue': 'Conference Room - Admin Block',
                'start_date': timezone.now() + timedelta(days=7),
                'end_date': timezone.now() + timedelta(days=9),
                'duration_hours': 20,
                'capacity': 40,
                'is_online': False,
                'prerequisites': 'Basic English communication, willingness to learn and participate',
                'learning_outcomes': 'Improve public speaking, master interview skills, develop professional etiquette, enhance teamwork abilities'
            },
            {
                'title': 'Interview Preparation Workshop',
                'description': 'Comprehensive interview preparation covering technical interviews, HR interviews, group discussions, and case studies. Practice mock interviews with industry experts and get personalized feedback.',
                'training_type': 'interview',
                'instructor': 'Industry Professionals',
                'venue': 'Training Room - Block C',
                'start_date': timezone.now() + timedelta(days=10),
                'end_date': timezone.now() + timedelta(days=11),
                'duration_hours': 16,
                'capacity': 35,
                'is_online': False,
                'prerequisites': 'Completed aptitude training, have basic technical knowledge',
                'learning_outcomes': 'Ace technical interviews, handle HR questions confidently, participate effectively in group discussions, solve case studies'
            },
            {
                'title': 'Cloud Computing with AWS',
                'description': 'Learn cloud computing fundamentals and AWS services. Master EC2, S3, Lambda, RDS, and other AWS services. Prepare for AWS Certified Solutions Architect certification with hands-on labs.',
                'training_type': 'technical',
                'instructor': 'Cloud Computing Experts',
                'venue': 'Online - AWS Academy Platform',
                'start_date': timezone.now() + timedelta(days=8),
                'end_date': timezone.now() + timedelta(days=15),
                'duration_hours': 30,
                'capacity': 45,
                'is_online': True,
                'meeting_link': 'https://aws.amazon.com/training/',
                'prerequisites': 'Basic networking knowledge, understanding of web applications',
                'learning_outcomes': 'Design and deploy cloud solutions, work with AWS services, prepare for AWS certification, implement cloud best practices'
            },
            {
                'title': 'Android App Development',
                'description': 'Learn to develop native Android applications using Java/Kotlin. Master Android Studio, UI design, database integration, APIs, and app deployment. Build real-world mobile applications.',
                'training_type': 'technical',
                'instructor': 'Mobile Development Institute',
                'venue': 'Mobile Lab - Block A',
                'start_date': timezone.now() + timedelta(days=12),
                'end_date': timezone.now() + timedelta(days=19),
                'duration_hours': 36,
                'capacity': 25,
                'is_online': False,
                'prerequisites': 'Java programming knowledge, understanding of OOP concepts',
                'learning_outcomes': 'Build Android apps, design mobile UI/UX, integrate databases, consume APIs, publish apps on Play Store'
            },
            {
                'title': 'Python Programming and Automation',
                'description': 'Master Python programming from basics to advanced concepts. Learn data structures, file handling, web scraping, automation, and scripting. Work on real-world automation projects.',
                'training_type': 'technical',
                'instructor': 'Python Programming Academy',
                'venue': 'Computer Lab - Block B',
                'start_date': timezone.now() + timedelta(days=4),
                'end_date': timezone.now() + timedelta(days=8),
                'duration_hours': 32,
                'capacity': 35,
                'is_online': False,
                'prerequisites': 'Basic programming concepts, logical thinking ability',
                'learning_outcomes': 'Write efficient Python code, automate tasks, work with data, develop applications, understand advanced Python features'
            },
            {
                'title': 'Resume Building and Personal Branding',
                'description': 'Create professional resumes, build your personal brand, optimize LinkedIn profile, and develop an online presence. Learn to showcase your skills effectively to recruiters.',
                'training_type': 'workshop',
                'instructor': 'Career Development Experts',
                'venue': 'Career Guidance Cell',
                'start_date': timezone.now() + timedelta(days=6),
                'end_date': timezone.now() + timedelta(days=6),
                'duration_hours': 8,
                'capacity': 50,
                'is_online': False,
                'prerequisites': 'Have basic academic information ready',
                'learning_outcomes': 'Create professional resumes, build personal brand, optimize online presence, attract recruiter attention'
            },
            {
                'title': 'Java Full Stack Development',
                'description': 'Comprehensive Java development training covering Core Java, Spring Boot, Hibernate, REST APIs, and frontend technologies. Build enterprise-level applications and microservices.',
                'training_type': 'technical',
                'instructor': 'Java Development Institute',
                'venue': 'Computer Lab - Block C',
                'start_date': timezone.now() + timedelta(days=14),
                'end_date': timezone.now() + timedelta(days=21),
                'duration_hours': 42,
                'capacity': 30,
                'is_online': False,
                'prerequisites': 'Basic programming knowledge, understanding of OOP concepts',
                'learning_outcomes': 'Develop Java applications, build REST APIs, work with databases, create microservices, understand enterprise architecture'
            }
        ]

        # Create training instances
        created_trainings = []
        for training_data in trainings:
            training = Training.objects.create(**training_data)
            created_trainings.append(training)
            self.stdout.write(
                self.style.SUCCESS(f'Created training: {training.title}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully populated {len(created_jobs)} jobs and {len(created_trainings)} training programs')
        )
