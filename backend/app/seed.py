from sqlmodel import Session, select

from backend.app.models import Plan, PlanCode


def seed_plans(session: Session) -> None:
    existing = {p.code for p in session.exec(select(Plan)).all()}
    plans = [
        Plan(
            code=PlanCode.FREE.value,
            name_en="Free",
            name_ar="مجاني",
            monthly_price=0,
            credits_per_month=25,
            max_watchlist=4,
            agents_enabled=True,
        ),
        Plan(
            code=PlanCode.PRO.value,
            name_en="Pro",
            name_ar="احترافي",
            monthly_price=29,
            credits_per_month=400,
            max_watchlist=25,
            agents_enabled=True,
        ),
        Plan(
            code=PlanCode.ELITE.value,
            name_en="Elite",
            name_ar="نخبة",
            monthly_price=99,
            credits_per_month=2500,
            max_watchlist=100,
            agents_enabled=True,
        ),
    ]
    for plan in plans:
        if plan.code not in existing:
            session.add(plan)
    session.commit()
