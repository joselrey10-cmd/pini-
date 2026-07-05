from pini_rule_engine.api.rule_api import RuleApi
from pini_rule_engine.services.rule_service import RuleService

def main() -> None:
    service = RuleService.create_in_memory()
    service.seed_default_rules()
    api = RuleApi(service)

    print("Pini 0.1 iniciado correctamente.")
    print("Rule Engine activo.")
    print(f"C006 máximo general: {api.get_parameter('C006', 'general_max_consecutive')}")
    print(f"Inglés 5º máximo consecutivas: {api.get_max_consecutive('Inglés', 5)}")
    print(f"Contextos después del recreo: {api.contexts_must_be_after_break()}")

if __name__ == "__main__":
    main()
