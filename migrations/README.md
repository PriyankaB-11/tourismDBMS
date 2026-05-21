Alembic migrations guidance

This project currently uses raw SQL DDL (see `database/schema.sql`). To add schema versioning with Alembic:

1) Install Alembic in your virtualenv:

```powershell
pip install alembic
```

2) Initialize Alembic (runs once):

```powershell
alembic init migrations/alembic
```

3) Configure `alembic.ini` and `env.py` to use the application's DB URL (read from environment variables or `config.py`).

4) Create an initial baseline migration (auto or manual):

```powershell
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

5) For small projects you may keep `database/schema.sql` as a reference; for ongoing development prefer migrations as the single source of truth.

Example migration snippet (auto-generated may look like):

```python
# revision: 12345
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('full_name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(120), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

def downgrade():
    op.drop_table('users')
```

Notes
- Triggers are MySQL-specific and cannot be fully represented via SQLAlchemy's higher-level API; you may include trigger creation SQL in raw statements within migrations (e.g., `op.execute("CREATE TRIGGER ...")`).
- Ensure tests run migrations in a disposable test database or use transactional rollbacks during testing.
