import com.fasterxml.jackson.annotation.JsonCreator;
import org.hyperledger.fabric.contract.annotation.DataType;
import org.hyperledger.fabric.contract.annotation.Property;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.util.UUID;

@DataType
@JsonPropertyOrder({"description", "id", "is_deleted", "name"})
public class Title {
    @Property
    @JsonProperty("id")
    private final UUID id;
    @Property
    @JsonProperty("name")
    private String name;
    @Property
    @JsonProperty("description")
    private String description;
    @Property
    @JsonProperty("is_deleted")
    private boolean is_deleted = false;
    @Property
    @JsonProperty("metatype")
    private final String metatype = "Title";

    @JsonCreator
    public Title(UUID id, String name, String description) {
        this.id = id;
        this.name = name;
        this.description = description;
    }

    public Title(){
        this.id = UUID.randomUUID();
    }

    public UUID getId() {
        return id;
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

    public boolean isIs_deleted() {
        return is_deleted;
    }

    public void setIs_deleted(boolean is_deleted) {
        this.is_deleted = is_deleted;
    }

    public String toJSONString() throws IOException {
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.writeValueAsString(this);
    }

    public static Title fromJSONString(String jsonString) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();

        return objectMapper.readValue(jsonString, Title.class);

    }
}