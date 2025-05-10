import React from "react";
import Link from "next/link";
import { FaTwitter } from "react-icons/fa";

export function Footer() {
  return (
    <footer className="mt-auto border-t-[3px] border-black py-4 lg:px-8">
      <div className="container mx-auto flex h-8 max-w-4xl items-center justify-center">
        <span className="text-sm font-medium text-black">
          Copyright © {" "}
          中南财经政法大学
        </span>
      </div>
    </footer>
  );
}