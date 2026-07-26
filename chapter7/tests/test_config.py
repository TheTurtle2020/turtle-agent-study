"""Config 组件的最小行为测试。"""

import pytest

from hello_agents import Config


def test_config_uses_teaching_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("DEBUG", "LOG_LEVEL", "TEMPERATURE", "MAX_TOKENS"):
        monkeypatch.delenv(name, raising=False)

    config = Config.from_env()

    assert config.default_model == "gpt-3.5-turbo"
    assert config.default_provider == "openai"
    assert config.temperature == 0.7
    assert config.max_tokens is None
    assert config.debug is False
    assert config.log_level == "INFO"
    assert config.max_history_length == 100


def test_config_reads_environment_overrides(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("TEMPERATURE", "0.2")
    monkeypatch.setenv("MAX_TOKENS", "256")

    config = Config.from_env()

    assert config.debug is True
    assert config.log_level == "DEBUG"
    assert config.temperature == 0.2
    assert config.max_tokens == 256


def test_config_to_dict_contains_all_fields() -> None:
    config = Config(temperature=0.1, max_tokens=64)

    assert config.to_dict() == {
        "default_model": "gpt-3.5-turbo",
        "default_provider": "openai",
        "temperature": 0.1,
        "max_tokens": 64,
        "debug": False,
        "log_level": "INFO",
        "max_history_length": 100,
    }


def test_config_fails_fast_on_invalid_numeric_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TEMPERATURE", "not-a-number")

    with pytest.raises(ValueError):
        Config.from_env()
