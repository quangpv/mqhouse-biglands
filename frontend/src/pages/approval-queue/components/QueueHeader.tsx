import { PageHeader } from "@/shared/components/page-header"

interface QueueHeaderProps {
  title: string
  pendingCount?: number
}

export function QueueHeader({ title, pendingCount }: QueueHeaderProps) {
  const desc = pendingCount !== undefined ? `${pendingCount} yêu cầu chờ duyệt` : undefined
  return <PageHeader title={title} description={desc} />
}
