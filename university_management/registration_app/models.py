from django.db import models
import uuid
import services_fabric


class Title(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Guardamos en la blockchain
        self.save_to_fabric()

    def save_to_fabric(self):
        # Llamada al servicio de Fabric para guardar el Title
        response = services_fabric.services_title.create_title({
            'id': str(self.id),
            'name': self.name,
            'description': self.description or ''
        })

        # Manejar la respuesta (puedes hacer logging o manejar errores)
        if response['status'] != '200':
            print(f"Error al guardar el título en la blockchain: {response}")

    def delete(self, *args, **kwargs):
        self.is_deleted = True  # Marca como eliminado
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
        # Luego guardamos en la blockchain
        self.save_to_fabric()

    def save_to_fabric(self):
        # Llamada al servicio de Fabric para guardar el Course
        response = services_fabric.services_course.create_course({
            'id': str(self.id),
            'title_id': str(self.title.primary_key),
            'name': self.name,
            'description': self.description or '',
            'start_date': str(self.start_date),
            'end_date': str(self.end_date)
        })

        # Manejar la respuesta (puedes hacer logging o manejar errores)
        if response['status'] != '200':
            print(f"Error al guardar el curso en la blockchain: {response}")

    def delete(self, *args, **kwargs):
        self.is_deleted = True  # Marca como eliminado
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
        # Luego guardamos en la blockchain
        self.save_to_fabric()

    def save_to_fabric(self):
        # Llamada al servicio de Fabric para guardar el Student
        response = services_fabric.services_student.create_student({
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        })

        # Manejar la respuesta (puedes hacer logging o manejar errores)
        if response['status'] != '200':
            print(f"Error al guardar el estudiante en la blockchain: {response}")

    def delete(self, *args, **kwargs):
        self.is_deleted = True  # Marca como eliminado
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
        # Luego guardamos en la blockchain
        self.save_to_fabric()

    def save_to_fabric(self):
        # Llamada al servicio de Fabric para guardar la Activity
        response = services_fabric.services_activity.create_activity({
            'id': str(self.id),
            'course_id': str(self.course.primary_key),
            'name': self.name,
            'description': self.description or '',
            'due_date': str(self.due_date)
        })

        # Manejar la respuesta (puedes hacer logging o manejar errores)
        if response['status'] != '200':
            print(f"Error al guardar la actividad en la blockchain: {response}")

    def delete(self, *args, **kwargs):
        self.is_deleted = True  # Marca como eliminado
        self.save()


class StudentActivityGrade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, related_name='grades', on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, related_name='student_grades', on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'activity')

    def __str__(self):
        return f"{self.student} - {self.activity}: {self.grade}"

    def save(self, *args, **kwargs):
        # Luego guardamos en la blockchain
        self.save_to_fabric()

    def save_to_fabric(self):
        # Llamada al servicio de Fabric para guardar el StudentActivityGrade
        response = services_fabric.services_student_activity_grade.create_student_activity_grade({
            'id': str(self.id),
            'student_id': str(self.student.primary_key),
            'activity_id': str(self.activity.primary_key),
            'grade': str(self.grade)
        })

        # Manejar la respuesta (puedes hacer logging o manejar errores)
        if response['status'] != '200':
            print(f"Error al guardar la calificación de actividad en la blockchain: {response}")

    def delete(self, *args, **kwargs):
        self.is_deleted = True  # Marca como eliminado
        self.save()
