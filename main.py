from src.agent import agent

EXIT_COMMANDS: frozenset[str] = frozenset({"sair", "exit", "quit", "q"})


def main() -> None:
    print("✅ Agente de Monitoramento com Ferramentas Pronto!")
    print("=" * 60)
    print("\n🤖 Agente DevOps - Analisador de Sistema")
    print("=" * 60)
    print("\nPergunta exemplos:")
    print("  • 'Como está o uso de CPU?'")
    print("  • 'Há problemas de memória?'")
    print("  • 'Qual é o status geral do sistema?'")
    print("  • 'Quais processos consomem mais memória?'")
    print(f"\nDigite {', '.join(sorted(EXIT_COMMANDS))} para finalizar\n")

    while True:
        try:
            pergunta = input("Você: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAté logo!")
            break

        if not pergunta:
            continue

        if pergunta.lower() in EXIT_COMMANDS:
            print("Até logo!")
            break

        try:
            resposta = agent.agent_check(pergunta)
            print(f"\nAgente: {resposta}\n")
        except KeyboardInterrupt:
            print("\n⏹️  Interrompido pelo usuário.\n")
        except Exception as e:
            print(f"❌ Erro: {e}")
            print("💡 Certifique-se que 'ollama serve' está rodando\n")


if __name__ == "__main__":
    main()