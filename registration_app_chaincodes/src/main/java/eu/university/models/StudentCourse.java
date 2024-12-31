package eu.university.models;

import java.util.UUID;

public class StudentCourse {
    private final UUID id;
    private Student student;
    private Course course;
    private double grade;
    private boolean is_deleted;

    public StudentCourse(UUID id, Student student, Course course, double grade) {
        this.id = id;
        this.student = student;
        this.course = course;
        this.grade = grade;
        this.is_deleted = false;
    }

    public UUID getId() {
        return id;
    }

    public Student getStudent() {
        return student;
    }

    public void setStudent(Student student) {
        this.student = student;
    }

    public Course getCourse() {
        return course;
    }

    public void setCourse(Course course) {
        this.course = course;
    }

    public double getGrade() {
        return grade;
    }

    public void setGrade(double grade) {
        this.grade = grade;
    }

    public boolean isIs_deleted() {
        return is_deleted;
    }

    public void setIs_deleted(boolean is_deleted) {
        this.is_deleted = is_deleted;
    }
}
