import React from "react";
import Link from "next/link";
import { ClerkProvider, SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/nextjs'

export async function Header() {
  return (
    <header className="border-b-[3px] border-black">
      <div className="mx-auto flex h-16 max-w-4xl items-center justify-between px-8">
        <Link href="/" className="flex items-center">
          <span className="text-xl font-semibold">
            <span className="text-black transition-colors duration-200 hover:text-gray-600">
              Git
            </span>
            <span className="text-orange-600 transition-colors duration-200 hover:text-orange-500">
              ToPod
            </span>
          </span>
        </Link>
        <nav className="flex items-center gap-6">
          <UserButton></UserButton>
        </nav>
      </div>
    </header>
  );
}