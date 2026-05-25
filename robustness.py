# Robustness Score Calculator


def calculate_robustness_score(

    walk_forward_efficiency,
    max_drawdown,
    consistency_score,
    parameter_stability

):

    # Weighted Robustness Formula
    robustness_score = (

        (walk_forward_efficiency * 0.40) +

        ((100 - max_drawdown) * 0.20) +

        (consistency_score * 0.20) +

        (parameter_stability * 0.20)

    )

    return round(
        robustness_score,
        2
    )


if __name__ == "__main__":

    # Example Values

    walk_forward_efficiency = 82

    max_drawdown = 12

    consistency_score = 85

    parameter_stability = 80

    # Calculate Robustness Score
    score = calculate_robustness_score(

        walk_forward_efficiency,

        max_drawdown,

        consistency_score,

        parameter_stability

    )

    print("\n========================")
    print(
        f"Robustness Score: "
        f"{score}"
    )

    # Strategy Evaluation
    if score >= 75:

        print(
            "Strategy is ROBUST "
            "and reliable."
        )

    else:

        print(
            "Strategy needs "
            "improvement."
        )

    print("========================")