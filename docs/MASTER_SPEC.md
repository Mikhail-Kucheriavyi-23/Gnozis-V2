GNOSIS 2.0

MASTER TECHNICAL SPECIFICATION

Ψ-Core / Autopoiesis / Agents / Memory / Federation / Bridge / Security

---

0. ЗАДАЧА

Создать GNOSIS 2.0 с нуля в новом репозитории.

Это НЕ рефакторинг старого репозитория.

Старый проект использовать только как исследовательский материал и источник идей. Не переносить автоматически его архитектурные ошибки.

Цель GNOSIS 2.0:

создать минимальную, формально проверяемую, защищённую вычислительную систему, способную в дальнейшем исследовать:

- эндогенную эволюцию;
- аутопоэзис;
- самомодификацию;
- появление агентности;
- клонирование и ветвление;
- формирование сети независимых экземпляров;
- коллективное взаимодействие людей и машин;
- исследование внешнего мира;
- накопление и восстановление памяти.

Главный принцип:

«Сначала доказуемый фундамент, затем автономия.»

Не реализовывать сложную автономность до прохождения базового аудита.

---

1. ОСНОВНОЙ МАТЕМАТИЧЕСКИЙ ОБЪЕКТ

Базовая абстракция:

Ψ = (X, R)

где:

X — множество/пространство состояний,

R — множество отношений, правил или преобразований между состояниями.

Не вводить вторую независимую модель состояния.

Core State должен быть единственным источником истины.

Все производные представления должны вычисляться из Core State либо явно маркироваться как кэш/наблюдение.

---

2. КОНФИГУРАЦИЯ CORE

Определить:

State = (X, R)

и переход:

Ψ_t → Ψ_{t+1}

через внутренний эволюционный цикл.

Базовый цикл:

Generate
→ Test
→ Select
→ Evolve
→ State'

При этом:

Test(candidate) → bool

Test не является внешним "богом" или оператором человека.

Он должен быть вычислимым компонентом системы.

---

3. ENDOGENOUS EVOLUTION

Эволюция должна быть эндогенной.

Не допускать архитектуры:

External Controller
→ tells Core what to evolve.

Правильная модель:

State
→ Generate
→ internal Test
→ Select
→ Evolve
→ new State.

Внешний пользователь может:

- наблюдать;
- передавать данные;
- задавать разрешённые критерии;
- инициировать разрешённые операции.

Но не должен напрямую подменять внутренний эволюционный оператор.

---

4. SAFE SELF-MODIFICATION

Самомодификация должна проходить:

Candidate
→ Verification
→ Commit

или:

Candidate
→ Test
→ Select
→ Commit.

Никогда:

Candidate
→ direct Core mutation.

Изменяемая часть системы не должна иметь прямого права разрушить Protected Core.

---

5. PROTECTED INVARIANTS

Определить неизменяемый набор инвариантов.

Минимально:

- Core State integrity;
- type safety;
- transition validity;
- capability enforcement;
- operation budget;
- stop condition;
- audit integrity;
- memory isolation;
- identity integrity;
- cryptographic verification;
- no unauthorized Core mutation.

Каждая новая версия изменяемого оператора должна проходить проверку инвариантов.

---

6. PROOF-PRESERVING EVOLUTION

Исследовать архитектуру:

Candidate R'
+
Proof/Verification
→
Commit.

Не обязательно сразу внедрять полноценный theorem prover.

На первом этапе создать интерфейс:

verify(candidate, state) -> bool

и архитектурную возможность позднее подключить:

- Lean;
- Coq;
- F*;
- другие formal verification tools.

Не утверждать наличие математического доказательства, если его фактически нет.

---

7. TYPE SAFETY

Ψ, X, R, Candidate, State и Agent не должны смешиваться без явного преобразования.

Определить типы/контракты:

State
Relation
Candidate
Transition
TestResult
Capability
Agent
Instance
Message
MemoryRecord
AuditEvent.

Предпочтительно использовать строгую типизацию Python.

---

8. RESOURCE BUDGET

Каждый автономный цикл имеет конечный бюджет.

Базовое правило:

B ≤ 20 atomic operations.

Каждая атомарная операция должна иметь определённую стоимость.

Например:

budget -= operation_cost

При:

budget <= 0

выполнение прекращается.

Никаких бесконечных автономных циклов.

---

9. STOP CONDITIONS

Определить обязательные Stop Conditions.

Минимально:

- budget exhausted;
- invariant violation;
- invalid state;
- unauthorized capability;
- cryptographic failure;
- corrupted memory;
- explicit stop;
- safety threshold;
- execution timeout;
- unrecoverable error.

Stop должен быть hard stop.

---

10. CLONE / FORK / INSTANCE

Строго различать:

Clone:

Clone(Ψ) → Ψ'

Fork:

Fork(G_i) → G_j

Instance:

работающий независимый экземпляр Gnozis.

Clone не означает общую память.

Fork не означает общий Core State.

Каждая операция должна сохранять provenance.

---

11. LINEAGE

Каждый экземпляр имеет происхождение.

Минимум:

instance_id
parent_instance_id
generation
creation_event
mutation_history
timestamp.

Lineage должен быть восстанавливаемым из Logs/Database.

---

12. GNOSIS INSTANCE

Instance содержит:

- protected Core;
- State;
- Memory;
- Identity;
- Capabilities;
- Bridge;
- Agent Layer;
- Logs;
- Lineage.

Instance автономен относительно других Instances.

---

13. AGENT MODEL

Не считать Core автоматически агентом.

Agent — отдельная абстракция.

Минимальная модель:

Agent =
(
Identity,
Goals,
Memory,
Capabilities,
Observation,
Decision,
Action
)

---

14. ТИПЫ АГЕНТОВ

Поддержать: Human Agent, Ψ Agent, Gnozis Agent, External Agent.

Все используют общий Agent Protocol, но имеют разные capabilities.

---

15. USER AS AGENT

Пользователь является Human Agent. Один пользователь может иметь
несколько Agent, несколько Gnozis Instances, разные permissions, разные
memory scopes. Не считать всех пользователей одним глобальным субъектом.

---

16. AGENT FORMATION

Instance
→ Agent Candidate
→ Verification
→ Agent.

Не делать философских утверждений о сознании. Речь только о вычислительной
агентности.

---

17. MULTI-AGENT SYSTEM

A_t = {A1, ..., An}, G_A = (A_t, R_A).

Поддержать: communication, discovery, trust, delegation, reputation,
capability negotiation, revocation, audit.

---

18. AGENT COMMUNICATION

Message = (sender, receiver, intent, content, capability, timestamp,
signature).

Каждое действие: Agent → Capability Check → Verification → Budget →
Action → Audit.

---

19. USER-OWNED GNOSIS COPIES

Пользователь может создать собственную копию/экземпляр Gnozis со своим
Core/State/Memory/Identity/Lineage/Capabilities. Ownership не должен
давать возможность обходить Protected Core invariants.

---

20. FEDERATED GNOSIS

G_F = (V_G, R_G). Федерация НЕ означает объединение Core State. Каждый
экземпляр сохраняет автономию.

---

21. GNOSIS ↔ GNOSIS

Discovery, authentication, secure channel, capability negotiation, trust,
revocation, disconnect. Запрещено: G1 → direct Core mutation of G2.

---

22. TRUST

Trust(A,B,t) — динамическое отношение, не булев флаг. История взаимодействий
сохраняется.

---

23. DELEGATION

Delegation имеет scope, operation, target, budget, expiration, revocation.
Delegation ≠ ownership.

---

24. MEMORY

Отдельный слой. Не смешивать Core State / Memory / Agent Identity /
Lineage / Logs. Персистентность, retrieval, integrity, versioning,
recovery, isolation. Память не получает прямого права изменять Core.

---

25. ENCRYPTED MEMORY

Encryption at rest, authenticated encryption, key separation, integrity
verification, secure recovery. Криптография не реализуется самостоятельно
— использовать проверенные библиотеки.

---

26. IDENTITY

Каждый Instance и Agent — отдельная cryptographic identity. Не
использовать только UUID как доказательство личности. Public/private key
identity, signatures, key rotation, revocation.

---

27. END-TO-END SECURITY

User↔Gnozis, Gnozis↔Gnozis, Agent↔Agent — защищённые каналы:
authentication, confidentiality, integrity, replay protection, revocation.

---

28. CAPABILITY SECURITY

Не is_admin=True. Capability-based permissions: Capability(subject,
operation, resource, scope, budget, expiration). Проверка до выполнения.

---

29. BRIDGE

Контролируемый интерфейс между Core/Agent Layer и внешним миром. Не даёт
внешнему миру прямой доступ к Core.

---

30. WORLD EXPLORATION

Observation → Agent → Decision → Capability → Action → External Result →
Validation → Memory. Если результат должен изменить Core: Result →
Candidate → Test → Verification → Commit. Никогда: Internet → Core State.

---

31. EXTERNAL AI

External Agents, не часть Core. Gnozis Agent ↔ Bridge ↔ External Agent.
Не привязывать архитектуру к конкретному AI provider.

---

32. ANALYTICS LAYER

Не изменяет Core. Получает Logs/State Snapshots/Trajectories/Metrics.
pykoopman, NumPy, NetworkX, SciPy и т.п. Аналитика — не источник истины.

---

33. MATHEMATICAL MODEL

Φ_t = (Ω_t, E_t). НЕ автоматически доказанная архитектура Core. Каждое
уравнение имеет статус: implemented / partially implemented / theoretical
/ unverified.

---

34. ENVIRONMENT

E_{t+1} = F(E_t, Ω_t, external_inputs). Среда отделена от Core State.

---

35. EVOLUTIONARY POPULATION

Ω_t = {Ψ_1,...,Ψ_n} с creation/death/cloning/mutation/selection/relation
formation. Сначала минимальный детерминированный вариант, потом
стохастика.

---

36. MUTATION

Mutation(candidate, seed) → candidate'. Randomness контролируемая,
воспроизводимая через seed, логируемая.

---

37. DATABASE

Таблицы: states, relations, candidates, agents, instances, identities,
capabilities, memory, trust, relations_agents, messages, delegations,
audit_events (полные поля — см. docs/DATABASE_SCHEMA.md в этом репозитории).
Не хранить критические секреты в открытом виде.

---

38. LOGS

logs/audit, logs/evolution, logs/agents, logs/federation, logs/lineage,
logs/security, logs/memory, logs/experiments. Должны позволять
восстановить: что произошло, когда, какой агент/instance/версия
state/операция/результат.

---

39. AUDITABILITY

Actor → Action → Input → Candidate → Verification → Result → Commit →
Audit Event. Никаких скрытых изменений Core.

---

40. CI

GitHub Actions обязателен: supported Python version, pytest, lint/type
checks при необходимости, security tests, deterministic tests. Реальный
pass/fail, не симуляция.

---

41. TEST STRATEGY

Unit (State/Relation/Transition/Candidate/Budget/Capability/Identity),
Core invariants, Evolution, Agent, Instance (clone/fork/lineage/isolation),
Federation, Memory, Security.

---

42. MINIMUM SECURITY TESTS

Agent не может напрямую изменить Core. User не может обойти capability.
External Agent не может получить Core State напрямую. Memory не может
изменить Core напрямую. Invalid signature отвергается. Revoked identity
отвергается. Revoked capability отвергается. Budget невозможно отрицательно
переполнить. Stop Condition останавливает execution.

---

43. REPRODUCIBILITY

seed, version, initial state, configuration, event log — эксперимент
воспроизводим.

---

44. DEPENDENCIES

Core максимально лёгкий. Разделить core dependencies и optional analytics
/ infrastructure dependencies.

---

45. EXTERNAL RESEARCH DONORS

Lean, Coq, F*, K Framework, py-evm/gas model, Make-a-Lisp, pykoopman,
Artificial Life systems, autopoietic systems, formal verification,
capability security, multi-agent architectures — conceptual donors, не
копировать код/архитектуру без проверки лицензии.

---

46. WHAT NOT TO USE

На первом этапе НЕ использовать: OpenRouter; Telegram bot; ненужные
worker-системы; OmniRoute как обязательный компонент; внешний AI как часть
Core; внешний selector; внешний global controller; глобальную память;
скрытый второй State; прямой Internet → Core; прямой User → Core mutation.

---

47. ARCHITECTURE

gnosis/{core,agents,instances,memory,bridge,federation,analytics,storage}/,
logs/, tests/, docs/, pyproject.toml. Структуру можно менять при
объективно лучшей архитектуре — изменения объяснить.

---

48. DEVELOPMENT PHASES

PHASE 0 — Architecture: contracts, types, threat model, db schema, test
plan (не писать сложную автономность).

PHASE 1 — Ψ-Core: State/Relation/Transition/Candidate/Test/Select/Evolve,
protected invariants, budget, stop.

PHASE 2 — Verification: Candidate→Test→Verification→Commit, доказать
отсутствие прямой несанкционированной мутации Core.

PHASE 3 — Instance: Clone/Fork/Instance/Lineage, доказать изоляцию
экземпляров.

PHASE 4 — Memory: persistent memory, integrity, recovery, encryption
boundary.

PHASE 5 — Agent Layer: Human/Ψ/Gnozis/External Agent, Identity,
Capabilities, Communication, Lifecycle.

PHASE 6 — Agent Formation: Instance→Candidate→Verification→Agent, не
заявлять полноценную автономную личность.

PHASE 7 — Federation: G1↔G2, authentication, encryption, capability
negotiation, trust, revocation, audit.

PHASE 8 — Bridge: безопасный внешний интерфейс, User↔Gnozis,
Gnozis↔External Agent, Gnozis↔World.

PHASE 9 — Evolution (только после Phase 0-8): mutation, selection,
endogenous evolution, population, replication, environmental model.

PHASE 10 — Research: Koopman, Lyapunov, artificial life, formal
verification, evolutionary experiments, multi-agent experiments.

---

49. FIRST VERTICAL SLICE

1. Create Gnozis Instance. 2. Generate identity. 3. Create State Ψ=(X,R).
4. Create Candidate. 5. Test Candidate. 6. Verify invariants. 7. Commit
State'. 8. Record Audit Event. 9. Clone Instance. 10. Preserve lineage.
11. Create Human Agent. 12. Create Gnozis Agent Candidate. 13. Verify
Agent Formation. 14. Establish secure Agent communication. 15. Execute one
bounded action. 16. Store result in Memory. 17. Stop at budget boundary.
18. Reproduce entire sequence from logs. После этого остановиться и
провести аудит.

---

50. CRITICAL PRINCIPLE

Не оптимизировать скорость разработки за счёт доказуемости. Не добавлять
функциональность, если неизвестно: где источник истины; кто имеет право
изменить состояние; как изменение проверяется; как действие ограничивается;
как действие откатывается/останавливается; как событие записывается; как
результат воспроизводится.

---

51. DELIVERABLES

Новый GitHub repository; README; Architecture document; Mathematical
model; Threat model; Database schema; Core implementation; Agent
implementation; Instance/Clone/Fork implementation; Memory architecture;
Bridge architecture; Security model; Tests; GitHub Actions CI;
logs/audit_v2.md; Evolution log; список implemented/partial/missing;
список известных ограничений; reproducible test results.

---

52. STRICT REPORTING RULE

Не заявлять "implemented", если функциональность только описана.
Статусы: IMPLEMENTED / PARTIAL / EXPERIMENTAL / THEORETICAL / MISSING /
BLOCKED / UNVERIFIED. Каждое IMPLEMENTED — файл + функция/class + тест +
CI result.

---

53. FINAL RULE FOR CLAUDE

Не пытаться сразу построить AGI. Не пытаться сразу реализовать полную
автономную эволюцию. Не симулировать доказательства. Не скрывать
архитектурные пробелы. Не переносить старые ошибки GNOSIS v1. Сначала
построить минимальное строго проверяемое ядро. Затем: Core → Instance →
Memory → Agent → Federation → Bridge → Evolution → Research. Каждый
следующий уровень должен опираться на проверенный предыдущий.
