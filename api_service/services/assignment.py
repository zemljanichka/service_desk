from database import AssignmentModel
from exeptions import UnauthorizedError
from schemas import Assignment, OperatorResponse, Ordering, Status


class AssignmentService:

    @staticmethod
    async def get_assignments(status: Status = None, order_by: Ordering = None):
        """Получение списка обращений с фильтрацией по статусу и времени"""
        if order_by == Ordering.asc:
            order = AssignmentModel.ts_created
        else:
            order = AssignmentModel.ts_created.desc()
        if status is not None:
            return await AssignmentModel.select(AssignmentModel.status == status, order_by=order)
        return await AssignmentModel.select(order_by=order)

    @staticmethod
    async def get_assignment_by_id(assignment_id: int):
        """Получение обращения по id"""
        return await AssignmentModel.get_single(AssignmentModel.id == assignment_id)

    @staticmethod
    async def create_assignment(assignment_data: dict):
        """Создание обращения в бд"""
        return await AssignmentModel.insert(**assignment_data)

    @staticmethod
    async def take_assignment(assignment_id: int, operator: OperatorResponse):
        """Присвоение обращению id оператора"""
        assignment = await AssignmentModel.get_single(AssignmentModel.id == assignment_id)
        if assignment.operator_id:
            raise UnauthorizedError
        new_status = AssignmentService.get_new_status(assignment)
        return await AssignmentModel.update(
            AssignmentModel.id == assignment_id,
            update_data={AssignmentModel.operator_id: operator.id, AssignmentModel.status: new_status},
        )

    @staticmethod
    async def change_status(assignment_id: int, operator: OperatorResponse):
        """Смена статуса обращения"""
        assignment = await AssignmentModel.get_single(AssignmentModel.id == assignment_id)
        if assignment.operator_id == operator.id:
            new_status = AssignmentService.get_new_status(assignment)
            return await AssignmentModel.update(
                AssignmentModel.id == assignment_id, update_data={AssignmentModel.status: new_status}
            )
        raise UnauthorizedError

    @staticmethod
    def get_new_status(assignment: Assignment):
        """Получение нового статуса"""
        match assignment.status:
            case Status.pending:
                return Status.processing
            case Status.processing:
                return Status.closed
            case Status.closed:
                raise ValueError
