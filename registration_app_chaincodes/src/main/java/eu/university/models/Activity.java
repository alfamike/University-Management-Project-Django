package eu.university.models;

import java.util.Date;
import java.util.UUID;

public class Activity {
    private final UUID id;
    private Course course;
    private String name;
    private String description;
    private Date due_date;
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
