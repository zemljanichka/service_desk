from database import AssignmentModel
from schemas import Assignment, OperatorResponse, Ordering, Status, AssignmentEmail


class AssignmentService:

    @staticmethod
    async def get_assignments(status: Status = None, order_by: Ordering = None):
        if order_by == Ordering.asc:
            order = AssignmentModel.ts_created
        else:
            order = AssignmentModel.ts_created.desc()
        if status is not None:
            return await AssignmentModel.select(AssignmentModel.status == status, order_by=order)
        return await AssignmentModel.select(order_by=order)

    @staticmethod
    async def get_assignment_by_id(assignment_id: int):
        return await AssignmentModel.get_single(AssignmentModel.id == assignment_id)

    @staticmethod
    async def create_assignment(assignment_data: dict):
        return await AssignmentModel.insert(**assignment_data)

    @staticmethod
    async def take_assignment(assignment_id: int, operator: OperatorResponse):
        assignment = await AssignmentModel.get_single(AssignmentModel.id == assignment_id)
        if assignment.operator_id:
            raise Exception
        new_status = AssignmentService.get_new_status(assignment)
        return await AssignmentModel.update(
            AssignmentModel.id == assignment_id, update_data={AssignmentModel.operator_id: operator.id, AssignmentModel.status: new_status}
        )

    @staticmethod
    async def change_status(assignment_id: int, operator: OperatorResponse):
        assignment = await AssignmentModel.get_single(AssignmentModel.id == assignment_id)
        if assignment.operator_id == operator.id:
            new_status = AssignmentService.get_new_status(assignment)
            return await AssignmentModel.update(AssignmentModel.id == assignment_id, update_data={AssignmentModel.status: new_status})
        raise Exception

    @staticmethod
    def get_new_status(assignment: Assignment):
        match assignment.status:
            case Status.pending:
                return Status.processing
            case Status.processing:
                return Status.closed
            case Status.closed:
                raise Exception