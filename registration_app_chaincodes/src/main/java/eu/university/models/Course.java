package eu.university.models;

import java.util.Date;
import java.util.UUID;

public class Course {
    private final UUID id;
    private Title title;
    private String name;
    private String description;
    private Date start_date;
    private Date end_date;
    private boolean is_deleted;

    public Course(UUID id, Title title, String name, String description, Date start_date, Date end_date) {
        this.id = id;
        this.title = title;
        this.name = name;
        this.description = description;
        this.start_date = start_date;
        this.end_date = end_date;
        this.is_deleted = false;
    }

    public UUID getId() {
        return id;
    }

    public Title getTitle() {
        return title;
    }

    public void setTitle(Title title) {
        this.title = title;
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

    public Date getStart_date() {
        return start_date;
    }

    public void setStart_date(Date start_date) {
        this.start_date = start_date;
    }

    public Date getEnd_date() {
        return end_date;
    }

    public void setEnd_date(Date end_date) {
        this.end_date = end_date;
    }

    public boolean isIs_deleted() {
        return is_deleted;
    }

    public void setIs_deleted(boolean is_deleted) {
        this.is_deleted = is_deleted;
    }
}
