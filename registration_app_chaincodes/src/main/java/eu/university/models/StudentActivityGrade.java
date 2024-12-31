package eu.university.models;

import java.util.UUID;

public class StudentActivityGrade {
    private final UUID id;
    private Student student;
    private Activity activity;
    private double grade;
    private boolean is_deleted;

    public StudentActivityGrade(UUID id, Student student, Activity activity, double grade) {
        this.id = id;
        this.student = student;
        this.activity = activity;
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

    public Activity getActivity() {
        return activity;
    }

    public void setActivity(Activity activity) {
        this.activity = activity;
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
