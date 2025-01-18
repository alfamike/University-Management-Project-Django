import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.hyperledger.fabric.contract.Context;
import org.hyperledger.fabric.contract.ContractInterface;
import org.hyperledger.fabric.contract.annotation.Contract;
import org.hyperledger.fabric.contract.annotation.Transaction;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import static java.nio.charset.StandardCharsets.UTF_8;

import java.io.IOException;

@Contract(name = "title_cc")
public class TitleChaincode implements ContractInterface {

    private final ObjectMapper objectMapper = new ObjectMapper();

    public TitleChaincode() {}

    private boolean titleExist(Context ctx, String titleId) {
        byte[] buffer = ctx.getStub().getState(titleId);
        return (buffer != null && buffer.length > 0);
    }

    private String createResponse(boolean success, String message) {
        try {
            Response response = new Response(success, message);
            return objectMapper.writeValueAsString(response);
        } catch (IOException e) {
            return createResponse(false, "Error serializing response");
        }
    }

    @Transaction(intent = Transaction.TYPE.SUBMIT)
    public String createTitle(Context ctx, UUID titleId, String titleName, String titleDescription) {
        boolean exists = titleExist(ctx, titleId.toString());

        if (exists) {
            return createResponse(false, "The title " + titleId + " already exists");
        }

        Title title = new Title(titleId, titleName, titleDescription);

        try {
            ctx.getStub().putState(titleId.toString(), title.toJSONString().getBytes(UTF_8));
            return createResponse(true, "Title created successfully");
        } catch (IOException e) {
            return createResponse(false, "Error creating title: " + e.getMessage());
        }
    }

    @Transaction(intent = Transaction.TYPE.EVALUATE)
    public String queryTitle(Context ctx, UUID titleId) {
        boolean exists = titleExist(ctx, titleId.toString());
        if (!exists) {
            return createResponse(false, "The title " + titleId + " does not exist");
        }
        return new String(ctx.getStub().getState(titleId.toString()), UTF_8);
    }

    @Transaction(intent = Transaction.TYPE.SUBMIT)
    public String updateTitle(Context ctx, UUID titleId, String name, String description) {
        boolean exists = titleExist(ctx, titleId.toString());
        if (!exists) {
            return createResponse(false, "The title " + titleId + " does not exist");
        }
        Title title = null;
        try {
            title = Title.fromJSONString(new String(ctx.getStub().getState(titleId.toString()), UTF_8));
            title.setName(name);
            title.setDescription(description);

            ctx.getStub().putState(titleId.toString(), title.toJSONString().getBytes(UTF_8));
            return createResponse(true, "Title updated successfully");
        } catch (IOException e) {
            return createResponse(false, "Error updating title: " + e.getMessage());
        }
    }

    @Transaction(intent = Transaction.TYPE.SUBMIT)
    public String deleteTitle(Context ctx, UUID titleId) {
        boolean exists = titleExist(ctx, titleId.toString());
        if (!exists) {
            return createResponse(false, "The title " + titleId + " does not exist");
        }
        Title title = null;
        try {
            title = Title.fromJSONString(new String(ctx.getStub().getState(titleId.toString()), UTF_8));
            title.setIs_deleted(false);
            ctx.getStub().putState(titleId.toString(), title.toJSONString().getBytes(UTF_8));
            return createResponse(true, "Title deleted successfully");
        } catch (IOException e) {
            return createResponse(false, "Error deleting title: " + e.getMessage());
        }
    }

    @Transaction(intent = Transaction.TYPE.EVALUATE)
    public String queryAllTitles(Context ctx) {
        List<Title> titles = new ArrayList<>();

        String queryString = "{\"selector\": {\"type\": \"Title\", \"is_deleted\": false}}";
        try {
            ctx.getStub().getQueryResult(queryString).forEach(kv -> {
                try {
                    Title title = Title.fromJSONString(new String(kv.getValue(), UTF_8));
                    titles.add(title);
                } catch (IOException e) {
                    throw new RuntimeException("Error parsing title during queryAllTitles: " + e.getMessage());
                }
            });

            String titlesJson = objectMapper.writeValueAsString(titles);

            return createResponse(true, titlesJson);
        } catch (RuntimeException e){
            return createResponse(false, "Error querying all titles: " + e.getMessage());
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    static class Response {
        private boolean success;
        private String message;

        public Response(boolean success, String message) {
            this.success = success;
            this.message = message;
        }

        // Getters and Setters
        public boolean isSuccess() {
            return success;
        }

        public void setSuccess(boolean success) {
            this.success = success;
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }
    }
}



