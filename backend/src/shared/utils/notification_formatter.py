TRANSACTION_LABELS: dict[str, str] = {
    "BAN": "Bán",
    "CHO_THUE": "Cho thuê",
    "SANG_NHUONG": "Sang nhượng",
}

ACTION_SUFFIX_MAP: dict[str, tuple[str, str]] = {
    "listing_post_created": ("vừa nhập", "chờ bạn duyệt"),
    "listing_post_approved": ("đã duyệt", "đã duyệt"),
    "listing_post_rejected": ("đã từ chối", ""),
    "deposit_reported": ("vừa chốt cọc", "chờ bạn duyệt"),
    "deposit_confirmed": ("đã duyệt chốt cọc", "đã duyệt"),
    "deposit_rejected": ("đã từ chối chốt cọc", ""),
    "closure_reported": ("vừa chốt hàng", "chờ bạn duyệt"),
    "closure_confirmed": ("đã duyệt chốt hàng", "đã duyệt"),
    "closure_rejected": ("đã từ chối chốt hàng", ""),
    "edit_rejected": ("đã từ chối chỉnh sửa", ""),
    "cancellation_reported": ("vừa hủy cọc", "chờ bạn duyệt"),
    "cancellation_confirmed": ("đã duyệt hủy cọc", "đã duyệt"),
    "cancellation_rejected": ("đã từ chối hủy cọc", ""),
    "sold_out_reported": ("vừa báo hết hàng", "chờ bạn duyệt"),
    "sold_out_confirmed": ("đã duyệt", "đã duyệt"),
    "sold_out_rejected": ("đã từ chối báo hết hàng", ""),
    "listing_updated": ("vừa chỉnh sửa", "chờ bạn duyệt"),
    "listing_expired": ("đã hết hạn", ""),
}


def format_notification_title(
    event_type: str,
    transaction_type: str | None,
    actor_name: str,
    item_code: str,
) -> str:
    action, suffix = ACTION_SUFFIX_MAP.get(event_type, ("", ""))
    category = TRANSACTION_LABELS.get(transaction_type or "", transaction_type or "")
    text = f"[{category}][{actor_name}] {action} mặt hàng [{item_code}]"
    if suffix:
        text += f", {suffix}"
    return text
