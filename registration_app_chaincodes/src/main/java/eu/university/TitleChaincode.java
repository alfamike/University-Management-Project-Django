package eu.university;

import eu.university.models.Title;
import org.hyperledger.fabric.contract.Context;
import org.hyperledger.fabric.contract.ContractInterface;
import org.hyperledger.fabric.contract.annotation.Contract;
import org.hyperledger.fabric.contract.annotation.Transaction;
import org.hyperledger.fabric.contract.routing.TransactionType;
import org.hyperledger.fabric.shim.ChaincodeStub;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import static java.nio.charset.StandardCharsets.UTF_8;

import java.io.IOException;

@Contract(name = "title_cc")
public class TitleChaincode implements ContractInterface {

    public TitleChaincode() {}

    private boolean titleExist(Context ctx, String titleId) {
        byte[] buffer = ctx.getStub().getState(titleId);
        return (buffer != null && buffer.length > 0);
    }

    @Transaction(intent = Transaction.TYPE.SUBMIT)
    public void createTitle(Context ctx, UUID titleId, String titleName, String titleDescription) {
        boolean exists = titleExist(ctx, titleId.toString());
        if (exists) {
            throw new RuntimeException("The title " + titleId.toString() + " already exists");
        }
        Title title = new Title(titleId, titleName, titleDescription);
        try {
            ctx.getStub().putState(titleId.toString(), title.toJSONString().getBytes(UTF_8));
        } catch (IOException e) {
            throw new RuntimeException("Error creating title: " + e.getMessage());
        }
    }

    @Transaction(intent = Transaction.TYPE.EVALUATE)
    public Title queryTitle(Context ctx, UUID titleId) {
        boolean exists = titleExist(ctx, titleId.toString());
        if (!exists) {
            throw new RuntimeException("The title " + titleId + " does not exist");
        }
        try {
            return Title.fromJSONString(new String(ctx.getStub().getState(titleId.toString()), UTF_8));
        } catch (IOException e) {
            throw new RuntimeException("Error querying title: " + e.getMessage());
        }
    }

    @Transaction(intent = Transaction.TYPE.SUBMIT)
    public void updateTitle(Context ctx, UUID titleId, String name, String description) {
        boolean exists = titleExist(ctx, titleId.toString());
        if (!exists) {
            throw new RuntimeException("The title " + titleId.toString() + " does not exist");
        }
        Title title = null;
        try {
            title = Title.fromJSONString(new String(ctx.getStub().getState(titleId.toString()), UTF_8));
            title.setName(name);
            title.setDescription(description);

            ctx.getStub().putState(titleId.toString(), title.toJSONString().getBytes(UTF_8));
        } catch (IOException e) {
            throw new RuntimeException("Error updating title: " + e.getMessage());
        }
    }

    @Transaction(intent = Transaction.TYPE.SUBMIT)
    public void deleteTitle(Context ctx, UUID titleId) {
        boolean exists = titleExist(ctx, titleId.toString());
        if (!exists) {
            throw new RuntimeException("The title " + titleId.toString() + " does not exist");
        }
        Title title = null;
        try {
            title = Title.fromJSONString(new String(ctx.getStub().getState(titleId.toString()), UTF_8));
            title.setIs_deleted(false);
            ctx.getStub().putState(titleId.toString(), title.toJSONString().getBytes(UTF_8));
        } catch (IOException e) {
            throw new RuntimeException("Error deleting title: " + e.getMessage());
        }
    }

    @Transaction(intent = Transaction.TYPE.EVALUATE)
    public List<Title> queryAllTitles(Context ctx) {
        List<Title> titles = new ArrayList<>();

        String queryString = "{\"selector\": {\"type\": \"Title\", \"is_deleted\": false}}";
        ctx.getStub().getQueryResult(queryString).forEach(kv -> {
            try {
                Title title = Title.fromJSONString(new String(kv.getValue(), UTF_8));
                titles.add(title);
            } catch (IOException e) {
                throw new RuntimeException("Error parsing title during queryAllTitles: " + e.getMessage());
            }
        });

        return titles; 
    }
}

