package eu.university;

public class activity_cc extends ChaincodeBase {

    @Override
    public Response init(ChaincodeStub stub) {
        return newSuccessResponse();
    }

    @Override
    public Response invoke(ChaincodeStub stub) {
        return newSuccessResponse();
    }

    public static void main(String[] args) {
        new activity_cc().start(args);
    }
    
}
