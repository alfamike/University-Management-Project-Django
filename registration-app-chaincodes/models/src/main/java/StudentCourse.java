import org.hyperledger.fabric.contract.annotation.DataType;
import org.hyperledger.fabric.contract.annotation.Property;

import java.util.UUID;

@DataType
public class StudentCourse {
    @Property
    private final UUID id;
    @Property
    private Student student;
    @Property
    private Course course;
    @Property
    private double grade;
    @Property
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
