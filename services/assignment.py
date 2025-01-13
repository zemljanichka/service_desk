from database import AssignmentModel
from schemas import Assignment


class AssignmentService:

    @staticmethod
    async def get_assignments():
        return await AssignmentModel.select()

    @staticmethod
    async def create_assignment(assignment_data: Assignment):
        return await AssignmentModel.insert(**assignment_data.dict())

    @staticmethod
    async def take_assignment(assignment_id: int, operator_id: int):
        return await AssignmentModel.update(
            AssignmentModel.id == assignment_id, update_data={AssignmentModel.operator_id: operator_id}
        )

    @staticmethod
    async def change_status(assignment_id: int):
        pass
