# IMRD TPO Admin Guide

## Admin Access

### Login Credentials
- **Email**: admin@imrd.edu.in
- **Password**: admin123
- **URL**: http://127.0.0.1:8000/admin/

## Admin Features

### 1. Training Management
The admin can add, edit, and manage training programs through the admin interface.

#### How to Add a New Training:
1. Login to admin panel
2. Go to "Trainings" section
3. Click "Add Training" button
4. Fill in the following details:

##### Training Information:
- **Title**: Training program name
- **Training Type**: Select from (Technical Skills, Soft Skills, Aptitude Training, Interview Preparation, Workshop, Certification, Other)
- **Instructor**: Trainer/Instructor name
- **Description**: Detailed description of the training

##### Schedule & Location:
- **Start Date**: Training start date and time
- **End Date**: Training end date and time
- **Duration Hours**: Total training duration in hours
- **Venue**: Training location or online platform
- **Is Online**: Check if it's an online training

##### Online Details (if online):
- **Meeting Link**: Online meeting link for virtual training

##### Capacity & Registration:
- **Capacity**: Maximum number of participants
- **Registered Count**: Auto-updated when students register
- **Is Active**: Whether registration is open

##### Learning Details:
- **Prerequisites**: Required knowledge or skills
- **Learning Outcomes**: What participants will learn

### 2. Job Management
Admin can also manage job opportunities:
- Add new job postings
- Edit existing jobs
- Manage deadlines and active status
- View job applications

### 3. User Management
- View all student profiles
- Manage user accounts
- Monitor placement status

## Default Data

The system comes pre-populated with:
- **10 Job Opportunities**: From companies like TCS, Infosys, Wipro, Microsoft, Google, Amazon, etc.
- **10 Training Programs**: Including Full Stack Development, Data Science, Aptitude Training, etc.

## Admin Panel Features

### Training Admin Interface:
- **List View**: Shows all trainings with title, type, instructor, dates, capacity, and registration status
- **Search**: Search by title, instructor, venue, or description
- **Filters**: Filter by training type, active status, online/offline, start date
- **Quick Edit**: Edit capacity and active status directly from list view
- **Fieldsets**: Organized form sections for easy data entry

### Key Features:
- **Real-time Updates**: Registration count updates automatically
- **Date Management**: Easy date/time selection
- **Online Support**: Separate fields for online meeting links
- **Capacity Management**: Track registered vs available slots
- **Status Control**: Activate/deactivate training registration

## Best Practices

1. **Clear Titles**: Use descriptive training titles
2. **Detailed Descriptions**: Provide comprehensive training descriptions
3. **Accurate Scheduling**: Set correct start/end dates and durations
4. **Prerequisites**: Clearly mention any required knowledge
5. **Learning Outcomes**: Specify what students will learn
6. **Capacity Planning**: Set realistic capacity limits
7. **Online Links**: Test meeting links before adding

## Student Experience

Students can:
- View all available trainings
- Register for trainings
- See training details and prerequisites
- Track their registered trainings
- Get training notifications

## Support

For any admin-related issues:
- Check the Django admin documentation
- Ensure proper date/time formats
- Verify meeting links for online trainings
- Monitor registration capacity
