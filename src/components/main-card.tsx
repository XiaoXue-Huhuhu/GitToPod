"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card } from "~/components/ui/card";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { Sparkles } from "lucide-react";
import React from "react";
import { CustomizationDropdown } from "./customization-dropdown";
import { exampleRepos } from "~/lib/exampleRepos";
import { useGlobalState } from "~/app/providers";
import { Label } from "~/components/ui/label";
import { RadioGroup, RadioGroupItem } from "~/components/ui/radio-group";
import { useAuth, SignInButton } from '@clerk/nextjs'

interface MainCardProps {
  isHome?: boolean;
  username?: string;
  repo?: string;
  showCustomization?: boolean;
  onModify?: (instructions: string) => void;
  onRegenerate?: (instructions: string) => void;
  onCopy?: () => void;
  lastGenerated?: Date;
}

export default function MainCard({
  isHome = true,
  username,
  repo,
  showCustomization,
  onModify,
  onRegenerate,
  onCopy,
  lastGenerated,
}: Readonly<MainCardProps>) {
  const { isLoaded, userId, sessionId, getToken } = useAuth()
  const { audioLength, setAudioLength, setAnotherVariable } = useGlobalState();
  const [repoUrl, setRepoUrl] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();
  const handleRadioChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (setAudioLength) {
        setAudioLength(event.target.value);
    } else {
        console.warn('setAudioLength is not defined');
    }
  };
  useEffect(() => {
    if (username && repo) {
      setRepoUrl(`https://github.com/ ${username}/${repo}`);
    }
  }, [username, repo, audioLength]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const githubUrlPattern =
      /^https?:\/\/github\.com\/([a-zA-Z0-9-_]+)\/([a-zA-Z0-9-_\.]+)\/?$/;
    const match = githubUrlPattern.exec(repoUrl.trim());

    if (!match) {
      setError("请输入有效的 GitHub 仓库 URL");
      return;
    }

    const [, username, repo] = match || [];
    if (!username || !repo) {
      setError("无效的仓库 URL 格式");
      return;
    }
    const sanitizedUsername = encodeURIComponent(username);
    const sanitizedRepo = encodeURIComponent(repo);


    // Just to trigger page reload on "Podcast" button press
    const randomNum = Math.floor(Math.random() * 10000000) + 1;
    setAnotherVariable(randomNum.toString());
    router.push(`/${sanitizedUsername}/${sanitizedRepo}`);
  };

  const handleExampleClick = (repoPath: string, e: React.MouseEvent) => {
    e.preventDefault();
    console.log(repoPath);
    router.push(repoPath);
  };

  return (
    <Card className="relative w-full max-w-3xl border-[3px] border-black bg-blue-100 p-4 shadow-[8px_8px_0_0_#000000] sm:p-8">
      <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-6">
        <div className="flex flex-col gap-3 sm:flex-row sm:gap-4">
          <Input
            placeholder="https://github.com/用户名/仓库名 "
            className="flex-1 rounded-md border-[3px] border-black px-3 py-4 text-base font-bold shadow-[4px_4px_0_0_#000000] placeholder:text-base placeholder:font-normal placeholder:text-gray-700 sm:px-4 sm:py-6 sm:text-lg sm:placeholder:text-lg"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            required
          />
          <Button
            type="submit"
            className="border-[3px] border-black bg-blue-300 p-4 px-4 text-base text-black shadow-[4px_4px_0_0_#000000] transition-transform hover:-translate-x-0.5 hover:-translate-y-0.5 hover:transform hover:bg-blue-300 sm:p-6 sm:px-6 sm:text-lg"
          >
            播客
          </Button>
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}
        <div>
        <RadioGroup
      defaultValue={audioLength}
      onValueChange={(value) => setAudioLength && setAudioLength(value)}
    >
      <div className="flex items-center space-x-2">
        <RadioGroupItem value="short" id="short" />
        <Label htmlFor="short">基础（约5分钟）</Label>
      </div>
      {userId ? ( // Check if user is authenticated
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="long" id="long" />
          <Label htmlFor="long">深入（约10分钟）</Label>
        </div>
      ) : (
        <div className="flex items-center space-x-2">
            <RadioGroupItem value="long" id="long" disabled/>
          <Label>深入（约10分钟） - </Label> <SignInButton><Button variant="outline" size={"sm"} className="h-6">登录以访问</Button></SignInButton>
        </div>
      )}
    </RadioGroup>

        </div>
        {showCustomization &&
          onModify &&
          onRegenerate &&
          onCopy &&
          lastGenerated && (
            <CustomizationDropdown
              onModify={onModify}
              onRegenerate={onRegenerate}
              onCopy={onCopy}
              lastGenerated={lastGenerated}
            />
          )}

        {/* Example Repositories */}
        {isHome && (
          <div className="space-y-2">
            <div className="text-sm text-gray-700 sm:text-base">
              尝试这些示例仓库：
            </div>
            <div className="flex flex-wrap gap-2">
              {Object.entries(exampleRepos).map(([name, path]) => (
                <Button
                  key={name}
                  variant="outline"
                  className="border-2 border-black bg-blue-300 text-sm text-black transition-transform hover:-translate-y-0.5 hover:transform hover:bg-blue-300 sm:text-base"
                  onClick={(e) => handleExampleClick(path, e)}
                >
                  {name}
                </Button>
              ))}
            </div>
          </div>
        )}
      </form>

      {/* Decorative Sparkle */}
      <div className="absolute -bottom-8 -left-12 hidden sm:block">
        <Sparkles
          className="h-20 w-20 fill-pink-300 text-black"
          strokeWidth={0.6}
          style={{ transform: "rotate(-15deg)" }}
        />
      </div>
    </Card>
  );
}