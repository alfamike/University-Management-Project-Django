package eu.university;

public class student_course_grade_cc extends ChaincodeBase {

    @Override
    public Response init(ChaincodeStub stub) {
        return newSuccessResponse();
    }

    @Override
    public Response invoke(ChaincodeStub stub) {
        return newSuccessResponse();
    }

    public static void main(String[] args) {
        new student_course_grade_cc().start(args);
    }
    
}
