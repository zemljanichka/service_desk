from database import AssignmentModel
from schemas import Assignment, OperatorResponse, Ordering, Status


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
    async def create_assignment(assignment_data: Assignment):
        return await AssignmentModel.insert(**assignment_data.dict())

    @staticmethod
    async def take_assignment(assignment_id: int, operator: OperatorResponse):
        return await AssignmentModel.update(
            AssignmentModel.id == assignment_id, update_data={AssignmentModel.operator_id: operator.id}
        )

    @staticmethod
    async def change_status(assignment_id: int):
        pass
