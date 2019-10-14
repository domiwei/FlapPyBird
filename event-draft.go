package main

import "fmt"

type Event struct {
}

type KVContainer interface {
	//Contain(key string) bool
	Get(key string) interface{}
}

type LeaderBoard struct { // implement KVContainer

}

type WhiteList struct { // implement KVContainer

}

// Constraint interface
type Constraint interface {
	Satisfy(event *Event) bool
}

// Define FilterConstraint
func NewContainConstraint(data KVContainer, field FilterField) (Constraint, error) {
	return &ContainConstraint{
		data:  data,
		field: field,
	}
}

type ContainConstraint struct {
	data  KVContainer
	field FilterField
}

func (fc *ContainConstraint) Satisfy(event *EventFlow) bool {
	if _, err := fc.data.Get(event.ReceiverID); err != nil {
		return false
	}
	return true
}

// End of definition of FilterConstraint

type Action struct {
	constraints Constraint
}

func (ac *Action) Act() error {
	if !constraints.Satisfy() {
		return fmt.Errorf("fail")
	}
	// TODO: update leaderboard
	return nil
}

type Dump struct {
	targetLeaderBoardName string
	constraints           Constraint
}

func (ac *Action) Dump() error {
	if !constraints.Satisfy() {
		return fmt.Errorf("fail")
	}
	// TODO: dump leaderboard
	return nil
}

func main() {
	fmt.Println("vim-go")
}
