import MainCard from "~/components/main-card";
import Hero from "~/components/hero";
import ProductHuntEmbed from "~/components/producthunt-embed";

export default function HomePage() {

  return (
    <main className="flex-grow px-8 pb-8 md:p-8">
      <div className="mx-auto mb-4 max-w-4xl lg:my-8">
        <Hero />
        <div className="mt-12"></div>
        <p className="mx-auto mt-8 max-w-2xl text-center text-lg">
        迅速将 GitHub 代码仓库转换为播客，把代码变成有声的故事。
        </p>
        <p className="mx-auto mt-0 max-w-2xl text-center text-lg">
          无论是通勤路上，还是休闲时光，轻松用耳朵了解代码，开启编程学习新方式。
        </p>
      </div>
      <div className="mb-16 flex flex-col items-center lg:mb-0">
        <MainCard/>
        <div className="mt-16">
            <ProductHuntEmbed />
        </div>
      </div>
    </main>
  );
}