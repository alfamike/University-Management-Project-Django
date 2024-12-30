package eu.university;

public class title_cc extends ChaincodeBase {

    @Override
    public Response init(ChaincodeStub stub) {
        return newSuccessResponse();
    }

    @Override
    public Response invoke(ChaincodeStub stub) {
        return newSuccessResponse();
    }

    public static void main(String[] args) {
        new title_cc().start(args);
    }
    
}
