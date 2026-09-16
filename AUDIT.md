# GNOZIS 2.0 — КОНТРОЛЬНЫЙ АУДИТ АКТУАЛЬНОСТИ АРХИВА

Аудируемый артефакт: `gnosis2-phase0-1-3.zip` (Phase 0 + Phase 1 + Phase 3 slice,
28 юнит-тестов, ~1065 строк кода в `gnosis/`).

Методология: код прочитан построчно; каждое требование проверено запуском
кода в песочнице (offline test runner + ad-hoc adversarial-скрипты), а не
только чтением файлов/README. Команды и результаты приведены как
доказательство, не как утверждение "должно работать".

**Ничего в архиве не изменено в ходе этого аудита.** Ниже — только анализ.

---

## 0. Ограничение проверки, которое нужно указать честно

В этой песочнице нет доступа в интернет, поэтому `pip install pytest`
не сработал. Тесты запущены через собственный офлайн-раннер
(`python3 run_tests.py`), который импортирует `tests/test_*.py` напрямую
и подсовывает минимальный shim вместо `pytest.raises`. Результат
идентичен по сути (28/28 assert-ов реально выполнились), но это **не**
прогон через настоящий `pytest`/CI, и GitHub Actions (`ci.yml`) в этой
песочнице не выполнялся вообще — его исправность подтверждена только
статическим чтением YAML, что по шкале раздела 29 — это "документация",
а не "исполненный код". Помечаю CI как **UNKNOWN** (не CONFLICT, но и не
IMPLEMENTED в терминах фактического запуска).

---

## 1. Итоговая таблица

| Requirement | Status | Evidence | Problem | Severity | Recommendation |
|---|---|---|---|---|---|
| Ψ=(X,R) единственный источник истины | IMPLEMENTED | `types.py::State` — один класс, нигде не дублируется | — | — | — |
| R может изменяться / стать ∅ | PARTIAL | `with_relations` добавляет; конструктор допускает `relations=()` | R нигде не трактуется как граф — единственный потребитель `.relations` — проверка "все ссылки валидны" (`invariants.py:59`) и копирование. Фактически близко к metadata-поле, не полноценному отношению | LOW | Если R нужен для будущей эволюции (mutation/selection по графу), заложить хотя бы один реальный consumer уже сейчас, иначе он останется decorative до Phase 9 |
| **Immutability (frozen=True) — реальная защита от мутации** | **CONFLICT** | Адверсариальный тест (см. §2 ниже): `state.elements['x']=1` мутирует State "на месте" без исключения; вложенный dict, полученный через `.elements`, мутируется и меняет `state_id` задним числом; `with_elements` шарит вложенные объекты между "версиями"; `Relation.value` хранит живую ссылку на объект вызывающего | `frozen=True` защищает только переприсваивание атрибута, не защищает содержимое `dict`/вложенных объектов — это ровно старый дефект v33 #8 "shallow frozen state" | **HIGH** | Не в рамках этого аудита — фиксирую как блокирующий дефект, требующий отдельного ТЗ на исправление (глубокое копирование / `types.MappingProxyType` / frozen recursive structures) |
| **Identity/no-op transition принимается как "эволюция"** | **CONFLICT** | Адверсариальный тест: candidate с версией `+1`, но идентичным содержимым `elements`/`relations` — принят, `state_id` изменился, `record.accepted=True` | Ни один инвариант не сравнивает фактическое содержимое до/после — только `state_integrity` (родитель) и `monotonic_version` (число). Это ровно старый дефект v33 #3 | **HIGH** | Нужен инвариант "meaningful change": сравнение content-hash elements/relations без учёта версии |
| Test(candidate) -> строгий bool | **CONFLICT** | Адверсариальный тест: `TestResult(passed='yes')` создаётся без ошибки и используется как истинное значение ниже по цепочке | Контракт `TestFn` и `TestResult.passed: bool` не проверяется в рантайме (только type hint) — ровно старый дефект v33 #6/#7 | **MEDIUM** (пока не эксплуатируется дефолтным `default_test`, но контракт открыт для любого кастомного `test_fn`) | Валидировать `isinstance(passed, bool)` в `TestResult.__post_init__` |
| Select (выбор среди кандидатов) | **MISSING** | В `Engine` нет ни одного метода, принимающего более одного `Candidate` | Заявленный в доке evolution.py цикл "Generate→Test→Select→Evolve" не содержит Select вообще — есть только Test→Evolve одного кандидата | HIGH (для доверия к формулировке "endogenous evolution cycle" в докстринге) | Пересмотреть докстринг evolution.py — он утверждает больше, чем реализовано |
| Generate — эндогенный, не внешний controller | **CONFLICT** с докстрингом | `Engine.run(generate_fn)` принимает функцию-генератор **снаружи** при каждом вызове `run()` | Докстринг evolution.py называет это "endogenous generator hook", но по факту это ровно паттерн "External Controller → tells Core what to evolve", который раздел 3 явно запрещает | MEDIUM | Либо переименовать/переформулировать докстринг (сейчас документация говорит больше, чем код), либо реализовать реальный внутренний generator как часть Core |
| Hidden mutable state (closures/globals/singleton) | NOT FOUND | Проверены все импорты и module-level присваивания в `gnosis/core` и `gnosis/instances`; `Budget`/`history` используют `default_factory`, отдельный объект на каждый `Engine` подтверждён тестом | — | — | — |
| Ports & Adapters / Core не зависит от адаптеров | IMPLEMENTED (тривиально) | `grep` импортов `gnosis/core/*.py` — только stdlib (`hashlib`,`json`,`dataclasses`,`enum`,`typing`) | Проверка тривиальна, т.к. адаптеров (Bridge/DB/HTTP) физически ещё не существует — направление зависимости не может быть нарушено при их отсутствии | — | Перепроверить, когда появится Phase 4/7/8 |
| OpenRouter / Bot отсутствуют как runtime-зависимость | IMPLEMENTED | Нет упоминаний ни в коде, ни в `pyproject.toml` | — | — | — |
| Memory как first-class компонент | MISSING | `gnosis/memory/` не существует физически (только упомянут в докстрингах как "Phase 4") | Соответствует STATUS.md, без расхождений | — | — |
| Database | SPEC_ONLY | `docs/DATABASE_SCHEMA.md` есть, `gnosis/storage/` — пустая директория, ни одного файла | — | — | — |
| **Logs (`logs/`)** | **CONFLICT с разделом 10** | `logs/audit`, `logs/evolution`, `logs/security` — три пустые директории, ни один Python-модуль в них не пишет | Ровно случай "не пустая директория и не декоративная папка" из требования — здесь она именно декоративная. Реальный "лог" — только `Engine.history` (`list[TransitionRecord]`), теряется при завершении процесса | **MEDIUM-HIGH** | Явно указать в STATUS.md/README, что `logs/` — placeholder, не функционирующий компонент (сейчас это подразумевается, но не сказано прямо) |
| Internet/User Bridge | MISSING | `gnosis/bridge/` не существует | Соответствует STATUS.md | — | — |
| Encryption/Security, fail-closed | UNKNOWN | Ни identity, ни auth, ни capability-проверок в коде нет вообще — "missing → True" паттерн физически негде обнаружить, т.к. нет ни одной проверки доверия | Нельзя подтвердить и нельзя опровергнуть fail-closed поведение на пустом множестве | — | Зафиксировать fail-closed как явное архитектурное требование ДО того, как появится первая проверка identity/capability (Phase 5) |
| Cloning / Lineage / Network | PARTIAL | `Instance.parent_instance_id`, `generation`, `ancestry_chain`, `descendants` — реализованы и протестированы (`test_instances.py`, 9 тестов) | Это лучше, чем "copy directory → независимая копия": provenance сохраняется. Но "connected network" (Instance ↔ Instance коммуникация) отсутствует полностью — lineage существует только как атрибуты данных, реестр (`registry: dict`) не персистентен, теряется при рестарте процесса | MEDIUM | Соответствует Phase 3/7 разделению — не блокирует, но зафиксировать, что "network" в смысле раздела 14 не начат |
| Multi-agent architectural readiness | **PARTIAL, слабее заявленного** | `types.py`: `Agent = None`, `Instance = None`, `Capability = None` и т.д. | Эти "forward stubs" — не типы и не Protocol, а буквально `None`. Их нельзя использовать как type hint для `isinstance`/наследования; это имя-заглушка, а не архитектурный контракт. Докстринг называет их "fixed contract to implement against" — это преувеличение | LOW-MEDIUM | Либо заменить на реальные `Protocol`/абстрактные классы (минимальная работа), либо явно понизить формулировку в докстринге до "имя зарезервировано, не является типом" |
| StopReason — 10 условий объявлены | **PARTIAL, слабее заявленного** | `grep StopReason.<X>` вне `types.py`: только `BUDGET_EXHAUSTED` (3 места) и `INVALID_STATE` (1 место) реально возбуждаются. Остальные 8 (`INVARIANT_VIOLATION`, `UNAUTHORIZED_CAPABILITY`, `CRYPTOGRAPHIC_FAILURE`, `CORRUPTED_MEMORY`, `EXPLICIT_STOP`, `SAFETY_THRESHOLD`, `EXECUTION_TIMEOUT`, `UNRECOVERABLE_ERROR`) нигде не возбуждаются | Само по себе ожидаемо для Phase 1 (большинство требует Agent/Memory/Identity слоёв), НО: `INVARIANT_VIOLATION` **должен** быть hard-stop-ом по тексту раздела 9, а в коде проваленный инвариант — это просто "rejected" кандидат, `Engine` продолжает работать как ни в чём не бывало | MEDIUM | Явное архитектурное решение нужно ДО Phase 5: "invariant failure = reject-this-candidate-and-continue" (текущее поведение) или "= hard stop всего Engine" (буквальное чтение раздела 9). Сейчас реализован первый вариант без явного обоснования разницы с требованием |
| Budget hard-stop | IMPLEMENTED | `test_budget_cannot_go_negative`, `test_budget_exhaustion_is_a_hard_stop` — оба реально выполнены | — | — | — |
| Gas-limited micro-VM / sandbox | MISSING | Нет исполнения кода вообще (Ψ-Core оперирует данными, не кодом) — концепция "gas на инструкцию" не применима, т.к. нет интерпретатора/VM | Ожидаемо для текущей фазы | — | — |
| Self-modification / immutable core boundary | MISSING (архитектурно не подготовлено) | Нет разделения "mutable workspace" vs "immutable core" как отдельного механизма — есть только общая неизменяемость `State`, которая сама оказалась дырявой (см. выше) | — | — | — |
| Test architecture — покрытие категорий | PARTIAL | Math invariants ✓, Evolution (частично, без Select/no-op) ✓, Lineage ✓. Immutability-тесты **дают ложную уверенность**: `test_state_is_immutable_container` проверяет только `AttributeError` при переприсваивании атрибута, не проверяет вложенную мутацию — то есть тест существует, но не доказывает то, что заявлено в его названии | Security/Persistence категории — MISSING (нечего тестировать, слои не существуют) | MEDIUM | Название `test_state_is_immutable_container` вводит в заблуждение относительно фактического покрытия |

---

## 2. Адверсариальные тесты иммутабельности (раздел 5) — фактические команды и вывод

```python
from gnosis.core import State

s0 = State(elements={'a': {'nested': 1}}, version=0)
before_id = s0.state_id
retrieved = s0.elements
retrieved['a']['nested'] = 999
after_id = s0.state_id
# -> before_id != after_id : True   (состояние ИЗМЕНИЛОСЬ задним числом)
# -> s0.elements['a']['nested'] == 999 : True

s1 = State(elements={'x': 1}, version=0)
s1.elements['y'] = 2
# -> succeeded, no exception; s1.elements == {'x': 1, 'y': 2}

s0 = State(elements={'a': {'count': 1}}, version=0)
s1 = s0.with_elements({'b': 2})
s1.elements['a']['count'] = 999
# -> s0.elements['a'] мутировал ТОЖЕ: {'count': 999}
# -> s0.elements['a'] is s1.elements['a'] : True (общая ссылка между "версиями")

shared_list = [1, 2, 3]
r = Relation(source='x', target='y', relation_type='rel', value=shared_list)
before = r.relation_id
shared_list.append(999)
after = r.relation_id
# -> r.value == [1, 2, 3, 999]  (Relation хранит живую ссылку, не снимок)
# -> before != after : True (relation_id "магически" меняется без явного изменения Relation)
```

Все четыре сценария выполнены реально в песочнице, вывод воспроизводим.
Это подтверждает **CONFLICT** со всем разделом 5 и является прямым
рецидивом дефекта v33 #8.

---

## 3. Раздел 25 — проверка на рецидивы v33 (построчно)

| OLD v33 DEFECT | FOUND IN 2.0? | FILE | LINE | SEVERITY | RECOMMENDATION |
|---|---|---|---|---|---|
| 1. duplicate State models | NO | — | — | — | — |
| 2. duplicate PsiTransition | NO | — | — | — | — |
| 3. identity transition | **YES** | `gnosis/core/invariants.py` (`check_monotonic_version`) + `evolution.py::Engine.step` | invariants.py:70-76 | HIGH | Добавить content-based "meaningful change" инвариант |
| 4. no-op methods | NO (не найдено явных pass-only методов) | — | — | — | — |
| 5. hidden mutable state | NO | — | — | — | проверено импортами и `default_factory` |
| 6. truthy Test instead of bool | **YES** (контрактно, не эксплуатируется дефолтным путём) | `gnosis/core/types.py::TestResult` | 128-136 | MEDIUM | `isinstance` проверка в `__post_init__` |
| 7. "bool" accepted as "int" | **YES** (тот же корень, что #6) | там же | там же | MEDIUM | там же |
| 8. shallow frozen state | **YES, подтверждено 4 адверсариальными тестами** | `gnosis/core/types.py::State.__post_init__`, `Relation` | 77-80, 38-60 | **HIGH** | Требует отдельного ТЗ на исправление до Phase 4 (Memory), иначе дефект унаследуется в persistence-слое |
| 9. fail-open authentication | UNKNOWN (нет ни одной auth-проверки, чтобы быть fail-open или fail-closed) | — | — | — | Зафиксировать требование заранее, до Phase 5 |
| 10. health endpoint claiming readiness | N/A (HTTP-слоя нет) | — | — | — | — |
| 11. adapter dependencies inside Core | NO | `gnosis/core/*.py` импортирует только stdlib | — | — | — |
| 12. multiple competing sources of truth | NO | — | — | — | — |
| 13. code existing but unused in runtime path | **YES** | `logs/` (пустые директории), 8 из 10 `StopReason` значений, `Agent/Instance/Capability/Message/MemoryRecord = None` заглушки | — | LOW-MEDIUM | Не критично для Phase 0-1 честности (задокументировано как THEORETICAL/MISSING в STATUS.md), но `logs/` конкретно нигде не помечен как "нефункциональный" явным текстом |

**Итог по разделу 25: 4 из 13 рецидивов старого проекта подтверждены** (пп. 3, 6/7 как один корень, 8, 13). Наиболее серьёзный — **#8 (shallow frozen state)**, т.к. он структурно совпадает с самым явным старым дефектом и ломает заявление "Core State — единственный источник истины, защищённый от побочной мутации".

---

## A. Что уже актуально

- Single-source-of-truth `State`, без дублирования модели.
- `Candidate → Test → Verify → Commit` как единственный путь изменения `Engine.state` — структурно верно, подтверждено тестом на отклонённого кандидата.
- Бюджет: hard-stop при исчерпании, отрицательное переполнение невозможно — подтверждено тестами.
- `Instance`/`Fork`/`Lineage`: изоляция состояния и бюджета между parent/child подтверждена адверсариальным тестом.
- Core не имеет ни одной внешней (не-stdlib) зависимости — направление зависимости Core←Adapters пока не нарушено просто потому, что адаптеров ещё нет.
- OpenRouter/Bot действительно отсутствуют как runtime-зависимость.

## B. Что устарело / не соответствует новому контрольному ТЗ

- Докстринг `evolution.py` заявляет "endogenous generator hook" — по факту генератор полностью внешний (`generate_fn` передаётся при каждом вызове `run()`), что новый аудит explicitly называет запрещённым паттерном (раздел 3).
- `types.py` называет `Agent/Instance/Capability/...` "forward stubs" — по факту это `None`, не тип и не контракт.
- Название теста `test_state_is_immutable_container` не соответствует тому, что тест на самом деле проверяет (только top-level reassignment, не глубокую мутацию).

## C. Что появилось после упаковки архива (новые/уточнённые требования контрольного ТЗ, которых не было в исходном мастер-ТЗ)

- Явное требование Ports & Adapters/Hexagonal Architecture с проверкой направления импортов (раздел 6) — в исходном ТЗ было только общее "не использовать X внутри Core" (раздел 46).
- Явная адверсариальная процедура проверки иммутабельности "создать → получить вложенный объект → изменить → проверить" (раздел 5) — в исходном ТЗ такой конкретной методологии не было.
- Концепция "gas-limited micro-VM" для будущего self-modification (раздел 21) — терминологически новая, в исходном ТЗ был только общий "budget".
- Явный запрет паттерна `missing → True` / требование fail-closed по умолчанию (раздел 13) — сформулировано жёстче, чем в исходном ТЗ.
- Полный чек-лист из 13 именованных рецидивов v33 (раздел 25) — в исходном ТЗ была только общая формулировка "не переносить архитектурные ошибки" (раздел 0/53).
- Требование реального запуска сборки/тестов с фиксацией команд и результатов как условие для любого статуса "IMPLEMENTED" (раздел 26/29) — раньше это подразумевалось разделом 52, но не было расписано как отдельная процедура аудита.
- Итоговая цветовая шкала вердикта 🟢/🟡/🟠/🔴 (раздел 30) — новый формат отчётности, не существовавший в исходном ТЗ.

## D. Что нужно добавить/исправить до начала дальнейшей разработки (блокирующее)

1. Реальная защита `State`/`Relation` от вложенной мутации (глубокое копирование или неизменяемые контейнеры на всех уровнях) — иначе Phase 4 (Memory/persistence) унаследует дырявую модель данных.
2. Инвариант "meaningful change", отклоняющий content-identical candidates, замаскированные под эволюцию.
3. Явное решение: invariant violation — это soft-reject (текущее поведение) или hard-stop всего Engine (буквальное требование раздела 9)? Нужно зафиксировать сознательно, а не по умолчанию.
4. Runtime-валидация `TestResult.passed` как строгого `bool`.

## E. Что можно отложить

- Настоящий `logs/`-writer с hash-chain — нужен до заявления "auditability", но не блокирует Phase 3/4 работу как таковую.
- Persistence лидерства (`ancestry_chain` переживает рестарт) — можно отложить до появления `gnosis/storage/`.
- Настоящие `Protocol`/абстрактные классы вместо `None`-заглушек для Agent/Capability/Message — можно отложить до Phase 5, но стоит хотя бы обновить докстринг раньше.
- Sandbox/gas-VM для self-modification — по спецификации это и так Phase 9+.

## F. Критические дефекты (подтверждены кодом/исполнением)

1. **Shallow frozen state** — `State`/`Relation` не защищены от мутации вложенных объектов (4 адверсариальных теста, раздел 2 выше). Рецидив v33 #8.
2. **Identity/no-op transition принимается как реальная эволюция** — content-identical candidate с бампнутой версией проходит все инварианты и коммитится. Рецидив v33 #3.
3. **`Test(candidate) -> bool` не enforced в рантайме** — `TestResult.passed` принимает любое truthy-значение без ошибки. Рецидив v33 #6/#7 (пока не эксплуатируется дефолтным `default_test`, но контракт открыт).

## G. Рекомендуемый следующий этап

Прежде чем продолжать по фазам (Identity → Agent → Federation → Bridge),
минимальный vertical slice из раздела 27.G контрольного ТЗ (`Ψ0 → Generate
→ Test → Select → Evolve → Ψ1 → Persist → Log → Recover`) **не может
считаться пройденным** в текущем архиве по трём причинам:

- Select отсутствует полностью;
- Persist/Recover отсутствуют полностью (нет `gnosis/storage/*.py`);
- Log — decorative (`logs/` пустой), реальный лог живёт только в памяти процесса.

Рекомендация: не расширять на Agent/Federation/Bridge, пока не закрыт
именно этот vertical slice целиком, включая три критических дефекта из
раздела F — иначе Persist/Recover будут строиться поверх модели данных,
которая, как показано выше, не является по-настоящему неизменяемой.

---

## Финальный вердикт

# 🟡 READY WITH ARCHITECTURAL PATCHES

Основная архитектура (single source of truth, Candidate→Test→Verify→Commit
как единственный путь мутации, изоляция Instance при fork) — правильная и
подтверждена исполняемыми тестами. Но три подтверждённых кодом дефекта
(shallow frozen state, identity-транзиты как ложная эволюция, unenforced
Test-контракт) — это не косметика, а прямые рецидивы именно тех классов
проблем, которые новое ТЗ требовало явно исключить. Ни один из них не
требует пересборки архитектуры с нуля (🟠/🔴) — все три чинятся в
пределах существующих модулей (`types.py`, `invariants.py`) без изменения
внешних контрактов `Engine`/`Instance`. Но их нельзя откладывать на потом:
Phase 4 (Memory/persistence) будет напрямую сериализовывать `State`, и
дырявая иммутабельность в этот момент станет намного дороже исправлять.
