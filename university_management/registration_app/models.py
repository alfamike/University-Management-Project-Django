import uuid

from django.db import models

from registration_app.services_fabric import services_title, services_course, services_student, services_activity, \
    services_student_activity_grade, services_student_course_grade


class Title(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check whether this is a new object or an update
        is_new = self._state.adding

        self.save_to_fabric(is_new)

    def save_to_fabric(self, is_new):

        title_data = {
            'id': str(self.id),
            'name': self.name,
            'description': self.description or ''
        }
        if is_new:
            response = services_title.create_title(title_data)
        else:
            response = services_title.update_title(title_id=str(self.id),
                                                   new_name=self.name,
                                                   new_description=self.description or ''
                                                   )

        if response['status'] != '200':
            print(f"Error saving the title in the blockchain: {response}")

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.ForeignKey(Title, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.title})"

    def save(self, *args, **kwargs):
        # Check whether this is a new object or an update
        is_new = self._state.adding

        self.save_to_fabric(is_new)

    def save_to_fabric(self, is_new):
        course_data = {
            'id': str(self.id),
            'title_id': str(self.title.primary_key),
            'name': self.name,
            'description': self.description or '',
            'start_date': str(self.start_date),
            'end_date': str(self.end_date)
        }
        if is_new:
            response = services_course.create_course(course_data)
        else:

            response = services_course.update_course(
                course_id=str(self.id),
                new_title_id=str(self.title.primary_key),
                new_name=self.name,
                new_description=self.description or '',
                new_start_date=str(self.start_date),
                new_end_date=str(self.end_date)
            )

        if response['status'] != '200':
            print(f"Error saving the course in the blockchain: {response}")

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    courses = models.ManyToManyField(Course, related_name='students')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Check whether this is a new object or an update
        is_new = self._state.adding

        self.save_to_fabric(is_new)

    def save_to_fabric(self, is_new):
        student_data = {
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }

        if is_new:
            response = services_student.create_student(student_data)
        else:
            response = services_student.update_student(
                student_id=str(self.id),
                new_first_name=self.first_name,
                new_last_name=self.last_name,
                new_email=self.email,
            )

        if response['status'] != '200':
            print(f"Error saving the students in the blockchain: {response}")

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, related_name='activities', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.course})"

    def save(self, *args, **kwargs):
        # Check whether this is a new object or an update
        is_new = self._state.adding

        self.save_to_fabric(is_new)

    def save_to_fabric(self, is_new):
        activity_data = {
            'id': str(self.id),
            'course_id': str(self.course.primary_key),
            'name': self.name,
            'description': self.description or '',
            'due_date': str(self.due_date),
        }

        # Call the appropriate Fabric service method
        if is_new:
            response = services_activity.create_activity(activity_data)
        else:
            response = services_activity.update_activity(
                activity_id=str(self.id),
                new_name=self.name,
                new_description=self.description or '',
                new_due_date=str(self.due_date),
            )

        # Handle response
        if response['status'] != '200':
            print(f"Error saving the activity in the blockchain: {response}")

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class StudentActivityGrade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, related_name='grades', on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, related_name='student_grades', on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'activity'], name='unique_student_activity')
        ]

    def __str__(self):
        return f"{self.student} - {self.activity}: {self.grade}"

    def save(self, *args, **kwargs):
        # Check whether this is a new object or an update
        is_new = self._state.adding

        self.save_to_fabric(is_new)

    def save_to_fabric(self, is_new):
        grade_data = {
            'student_id': str(self.student.primary_key),
            'activity_id': str(self.activity.primary_key),
            'grade': str(self.grade),
        }

        if is_new:
            response = services_student_activity_grade.create_student_activity_grade(grade_data)
        else:
            response = services_student_activity_grade.update_student_activity_grade(
                student_id=str(self.student.primary_key),
                activity_id=str(self.activity.primary_key),
                new_grade=str(self.grade),
            )

        # Handle response
        if response['status'] != '200':
            print(f"Error saving grade in the blockchain: {response}")

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class StudentCourseGrade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, related_name='course_grades', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='student_grades', on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True,
                                null=True)  # Allow grades to be optional initially
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_student_course')
        ]

    def __str__(self):
        return f"{self.student} - {self.course}: {self.grade}"

    def save(self, *args, **kwargs):
        # Check whether this is a new object or an update
        is_new = self._state.adding

        self.save_to_fabric(is_new)

    def save_to_fabric(self, is_new):
        grade_data = {
            'student_id': str(self.student.primary_key),
            'course_id': str(self.course.primary_key),
            'grade': str(self.grade),
        }

        if is_new:
            response = services_student_course_grade.create_student_course_grade(grade_data)
        else:
            response = services_student_course_grade.update_student_course_grade(
                student_id=str(self.student.primary_key),
                course_id=str(self.course.primary_key),
                new_grade=str(self.grade),
            )

        if response['status'] != '200':
            print(f"Error saving course grade in the blockchain: {response}")

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
