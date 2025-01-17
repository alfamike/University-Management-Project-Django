import org.hyperledger.fabric.contract.annotation.DataType;
import org.hyperledger.fabric.contract.annotation.Property;

import java.util.Date;
import java.util.UUID;

@DataType
public class Activity {
    @Property
    private final UUID id;
    @Property
    private Course course;
    @Property
    private String name;
    @Property
    private String description;
    @Property
    private Date due_date;
    @Property
    private boolean is_deleted;

    public Activity(UUID id, Course course, String name, String description, Date due_date) {
        this.id = id;
        this.course = course;
        this.name = name;
        this.description = description;
        this.due_date = due_date;
        this.is_deleted = false;
    }

    public UUID getId() {
        return id;
    }

    public Course getCourse() {
        return course;
    }

    public void setCourse(Course course) {
        this.course = course;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Date getDue_date() {
        return due_date;
    }

    public void setDue_date(Date due_date) {
        this.due_date = due_date;
    }

    public boolean isIs_deleted() {
        return is_deleted;
    }

    public void setIs_deleted(boolean is_deleted) {
        this.is_deleted = is_deleted;
    }
}
