import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

# In a real clinical system, this would write to a secure, append-only datastore or SIEM.
# For this phase, we use structured Python logging.
logger = logging.getLogger("clinical_audit")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - AUDIT - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def log_clinical_action(
    clinician_id: uuid.UUID,
    action: str,
    target_entity: str,
    target_id: Optional[uuid.UUID] = None,
    details: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Records a strict audit log of any access or mutation of clinical data.
    """
    audit_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "clinician_id": str(clinician_id),
        "action": action,
        "target_entity": target_entity,
        "target_id": str(target_id) if target_id else None,
        "details": details or {},
    }

    # Do NOT log PII or raw clinical note content in the audit log.
    # Only log identifiers and actions.
    logger.info(str(audit_entry))
