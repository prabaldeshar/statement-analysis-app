import { cn } from "@/lib/utils"

export function Spinner({ size = "md", variant = "primary", className, ...props }) {
  const sizeClasses = {
    sm: "h-4 w-4 border-2",
    md: "h-6 w-6 border-2",
    lg: "h-8 w-8 border-3",
    xl: "h-12 w-12 border-4",
  }

  const variantClasses = {
    primary: "border-primary border-t-transparent",
    secondary: "border-secondary border-t-transparent",
    accent: "border-accent border-t-transparent",
    white: "border-white border-t-transparent",
  }

  return (
    <div
      className={cn("animate-spin rounded-full", sizeClasses[size], variantClasses[variant], className)}
      {...props}
      role="status"
      aria-label="Loading"
    />
  )
}

