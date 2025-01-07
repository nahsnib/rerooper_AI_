// 主要規則表框架

// 規則表主體
class RuleTable {
    constructor() {
        this.mainRules = []; // 主規則Y列表
        this.subRules = [];  // 副規則X列表
    }

    // 新增主規則
    addMainRule(rule) {
        this.mainRules.push(rule);
    }

    // 新增副規則
    addSubRule(rule) {
        this.subRules.push(rule);
    }

    // 顯示所有規則
    displayRules() {
        console.log("主規則:");
        this.mainRules.forEach((rule, index) => {
            console.log(`${index + 1}. ${rule.name}: ${rule.description}`);
        });
        console.log("副規則:");
        this.subRules.forEach((rule, index) => {
            console.log(`${index + 1}. ${rule.name}: ${rule.description}`);
        });
    }
}

// 事件類
class Event {
    constructor(name, effect) {
        this.name = name; // 事件名稱
        this.effect = effect; // 事件效果描述
    }
}

// 身分類
class Role {
    constructor(name, traits = [], abilities = []) {
        this.name = name; // 身分名稱
        this.traits = traits; // 特性列表
        this.abilities = abilities; // 能力列表
    }

    // 新增特性
    addTrait(trait) {
        this.traits.push(trait);
    }

    // 新增能力
    addAbility(ability) {
        this.abilities.push(ability);
    }
}

// 規則類
class Rule {
    constructor(name, description, specialConditions = [], roles = []) {
        this.name = name; // 規則名稱
        this.description = description; // 規則描述
        this.specialConditions = specialConditions; // 特殊條件列表
        this.roles = roles; // 涉及的身分列表
    }

    // 新增特殊條件
    addSpecialCondition(condition) {
        this.specialConditions.push(condition);
    }

    // 新增相關身分
    addRole(role) {
        this.roles.push(role);
    }
}

// 能力類
class Ability {
    constructor(name, type, effect) {
        this.name = name; // 能力名稱
        this.type = type; // 能力類型 ("主動" 或 "被動")
        this.effect = effect; // 能力效果描述
    }
}
