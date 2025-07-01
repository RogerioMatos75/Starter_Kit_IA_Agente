/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configura a saída para exportação estática, que gera arquivos HTML/CSS/JS puros.
  output: 'export',

  // Desabilita a otimização de imagens do Next.js, pois não teremos um servidor Node.js rodando.
  // Isso garante que as imagens funcionem corretamente na exportação estática.
  images: {
    unoptimized: true,
  },
};

export default nextConfig;