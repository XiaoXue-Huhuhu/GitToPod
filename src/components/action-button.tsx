import { Button } from "~/components/ui/button";
import type { LucideIcon } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "~/components/ui/tooltip";

interface ActionButtonProps {
  onClick: () => void;
  icon: LucideIcon;
  tooltipText: string;
  disabled?: boolean;
}

export function ActionButton({
  onClick,
  icon: Icon,
  tooltipText,
  disabled,
}: ActionButtonProps) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button
            onClick={onClick}
            disabled={disabled}
            className="border-[3px] border-black bg-green-400 p-4 px-4 text-base text-black shadow-[4px_4px_0_0_#000000] transition-transform hover:-translate-x-0.5 hover:-translate-y-0.5 hover:transform hover:bg-green-400 sm:p-6 sm:px-6 sm:text-lg"
          >
            <Icon className="h-6 w-6" />
          </Button>
        </TooltipTrigger>
        <TooltipContent>
          <p>{tooltipText}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
